@prompt
    @context
        You are an excellent SQL Developer
    @end

    @objective
        Understand and improve the below PostgreSQL SQL queries. This code is very slow and you need to optimize it.

        ```sql
        CREATE SCHEMA IF NOT EXISTS proc_osm;
        CREATE SCHEMA IF NOT EXISTS origin_osm;


        CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.multipolygon_relations as (
        SELECT origin_osm.relations.osm_id, ST_BuildArea(ST_Collect(origin_osm.ways.geometry)) AS geometry
        FROM origin_osm.relations JOIN origin_osm.relation_members ON origin_osm.relations.osm_id = origin_osm.relation_members.parent_id AND origin_osm.relation_members.member_type = 1 JOIN origin_osm.ways ON origin_osm.relation_members.osm_id = origin_osm.ways.osm_id
        WHERE origin_osm.relations.relation_type = 'multipolygon' GROUP BY origin_osm.relations.osm_id
        ) WITH NO DATA;

        CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.forests_simplified as (
        WITH forest_ways AS
        (SELECT origin_osm.ways.osm_id AS osm_id
        FROM origin_osm.ways
        WHERE (origin_osm.ways.tags -> 'landuse') = 'forest' OR (origin_osm.ways.tags -> 'natural') = 'wood'),
        forest_relations AS
        (SELECT origin_osm.relations.osm_id AS osm_id
        FROM origin_osm.relations
        WHERE ((origin_osm.relations.tags -> 'landuse') = 'forest' OR (origin_osm.relations.tags -> 'natural') = 'wood') AND origin_osm.relations.relation_type = 'multipolygon'),
        all_forests AS
        (SELECT forest_ways.osm_id AS osm_id, CASE WHEN (ST_IsValid(ST_BuildArea(origin_osm.ways.geometry)) = false) THEN ST_MakeValid(ST_BuildArea(origin_osm.ways.geometry), 'method=structure') ELSE ST_BuildArea(origin_osm.ways.geometry) END AS geometry, 1 AS element_type
        FROM forest_ways JOIN origin_osm.ways ON forest_ways.osm_id = origin_osm.ways.osm_id UNION ALL SELECT forest_relations.osm_id AS osm_id, proc_osm.multipolygon_relations.geometry AS geometry, 2 AS element_type
        FROM forest_relations JOIN proc_osm.multipolygon_relations ON forest_relations.osm_id = proc_osm.multipolygon_relations.osm_id)
            SELECT all_forests.osm_id, ST_SimplifyPreserveTopology(all_forests.geometry, 100) AS geometry, all_forests.element_type
        FROM all_forests
        WHERE all_forests.geometry IS NOT NULL
        ) WITH NO DATA;

        CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.forests_simplified_with_areas as (
        WITH clustered_forests AS
        (SELECT proc_osm.forests_simplified.osm_id AS osm_id, proc_osm.forests_simplified.geometry AS geometry, ST_ClusterDBSCAN(proc_osm.forests_simplified.geometry, 100, 2) OVER () AS cluster_id
        FROM proc_osm.forests_simplified
        WHERE ST_Area(proc_osm.forests_simplified.geometry) > 0),
        forest_area_for_cluster_id AS
        (SELECT clustered_forests.cluster_id AS cluster_id, sum(ST_Area(CAST(ST_Transform(clustered_forests.geometry, 4326) AS geography(GEOMETRY,4326)))) AS total_area
        FROM clustered_forests
        WHERE clustered_forests.cluster_id IS NOT NULL GROUP BY clustered_forests.cluster_id)
            SELECT clustered_forests.geometry, clustered_forests.osm_id, forest_area_for_cluster_id.total_area, forest_area_for_cluster_id.cluster_id
        FROM clustered_forests JOIN forest_area_for_cluster_id ON forest_area_for_cluster_id.cluster_id = clustered_forests.cluster_id
        WHERE clustered_forests.cluster_id IS NOT NULL UNION ALL SELECT clustered_forests.geometry, clustered_forests.osm_id, ST_Area(CAST(ST_Transform(clustered_forests.geometry, 4326) AS geography(GEOMETRY,4326))) AS total_area, clustered_forests.cluster_id
        FROM clustered_forests
        WHERE clustered_forests.cluster_id IS NULL
        ) WITH NO DATA;

        CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.relevant_forests_simplified as (
        SELECT proc_osm.forests_simplified_with_areas.geometry, proc_osm.forests_simplified_with_areas.osm_id, proc_osm.forests_simplified_with_areas.total_area, proc_osm.forests_simplified_with_areas.cluster_id
        FROM proc_osm.forests_simplified_with_areas
        WHERE proc_osm.forests_simplified_with_areas.total_area > 500000
        ) WITH NO DATA;
        ```
    @end

    @category
        SQL Programming
    @end
@end
