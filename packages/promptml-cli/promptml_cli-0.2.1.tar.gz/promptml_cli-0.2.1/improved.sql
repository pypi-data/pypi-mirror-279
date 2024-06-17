
 -- Create indexes to speed up queries
CREATE INDEX idx_relations_osm_id ON origin_osm.relations(osm_id);
CREATE INDEX idx_relation_members_parent_id ON origin_osm.relation_members(parent_id);
CREATE INDEX idx_relation_members_osm_id ON origin_osm.relation_members(osm_id);
CREATE INDEX idx_relation_members_member_type ON origin_osm.relation_members(member_type);
CREATE INDEX idx_ways_osm_id ON origin_osm.ways(osm_id);
CREATE INDEX idx_ways_tags_landuse ON origin_osm.ways USING GIN (tags);
CREATE INDEX idx_relations_tags_landuse ON origin_osm.relations USING GIN (tags);
CREATE INDEX idx_forests_simplified_geometry ON proc_osm.forests_simplified USING GIST (geometry);
CREATE INDEX idx_forests_simplified_area ON proc_osm.forests_simplified USING BTREE (ST_Area(geometry));


-- Create materialized views
CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.multipolygon_relations AS (
    SELECT r.osm_id, ST_BuildArea(ST_Collect(w.geometry)) AS geometry
    FROM origin_osm.relations r
    JOIN origin_osm.relation_members rm ON r.osm_id = rm.parent_id AND rm.member_type = 1
    JOIN origin_osm.ways w ON rm.osm_id = w.osm_id
    WHERE r.relation_type = 'multipolygon'
    GROUP BY r.osm_id
) WITH NO DATA;

 -- Create materialized view for forests
CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.forests_simplified AS (
    WITH forest_ways AS (
        SELECT w.osm_id
        FROM origin_osm.ways w
        WHERE w.tags -> 'landuse' = 'forest' OR w.tags -> 'natural' = 'wood'
    ),
    forest_relations AS (
        SELECT r.osm_id
        FROM origin_osm.relations r
        WHERE (r.tags -> 'landuse' = 'forest' OR r.tags -> 'natural' = 'wood')
        AND r.relation_type = 'multipolygon'
    ),
    all_forests AS (
        SELECT w.osm_id,
                CASE WHEN NOT ST_IsValid(ST_BuildArea(w.geometry)) THEN
                    ST_MakeValid(ST_BuildArea(w.geometry), 'method=structure')
                ELSE ST_BuildArea(w.geometry)
                END AS geometry,
                1 AS element_type
        FROM forest_ways
        JOIN origin_osm.ways w ON forest_ways.osm_id = w.osm_id
        UNION ALL
        SELECT fr.osm_id,
                m.geometry,
                2 AS element_type
        FROM forest_relations fr
        JOIN proc_osm.multipolygon_relations m ON fr.osm_id = m.osm_id
    )
    SELECT af.osm_id,
            ST_SimplifyPreserveTopology(af.geometry, 100) AS geometry,
            af.element_type
    FROM all_forests af
    WHERE af.geometry IS NOT NULL
) WITH NO DATA;

-- Create materialized view for forests with areas
CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.forests_simplified_with_areas AS (
    WITH clustered_forests AS (
        SELECT fs.osm_id,
                fs.geometry,
                ST_ClusterDBSCAN(fs.geometry, 100, 2) OVER () AS cluster_id
        FROM proc_osm.forests_simplified fs
        WHERE ST_Area(fs.geometry) > 0
    ),
    forest_area_for_cluster_id AS (
        SELECT cf.cluster_id,
                SUM(ST_Area(ST_Transform(cf.geometry, 4326)::geography)) AS total_area
        FROM clustered_forests cf
        WHERE cf.cluster_id IS NOT NULL
        GROUP BY cf.cluster_id
    )
    SELECT cf.geometry,
            cf.osm_id,
            COALESCE(fa.total_area, ST_Area(ST_Transform(cf.geometry, 4326)::geography)) AS total_area,
            cf.cluster_id
    FROM clustered_forests cf
    LEFT JOIN forest_area_for_cluster_id fa ON fa.cluster_id = cf.cluster_id
) WITH NO DATA;

-- Create materialized view for relevant forests
CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.relevant_forests_simplified AS (
    SELECT fsa.geometry,
        fsa.osm_id,
        fsa.total_area,
        fsa.cluster_id
    FROM proc_osm.forests_simplified_with_areas fsa
    WHERE fsa.total_area > 500000
) WITH NO DATA;
