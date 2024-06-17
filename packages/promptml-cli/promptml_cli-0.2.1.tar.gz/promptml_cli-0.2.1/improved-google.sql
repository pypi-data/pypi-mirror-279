
 -- Optimization Strategy:

 -- 1. Minimize CTEs and Subqueries: Combine CTEs where possible to reduce redundant scans and materialization.
 -- 2. Index Strategically: Add indexes on frequently used columns in joins and WHERE clauses.
 -- 3. Simplify Logic: Eliminate unnecessary operations and conditions.
 -- 4. Combine Geometries Early: Perform ST_BuildArea and ST_SimplifyPreserveTopology earlier in the process to reduce the size of intermediate data.

 CREATE SCHEMA IF NOT EXISTS proc_osm;
 CREATE SCHEMA IF NOT EXISTS origin_osm;

 -- Assuming origin_osm.relations.osm_id, origin_osm.relation_members.parent_id,
 -- origin_osm.relation_members.osm_id and origin_osm.ways.osm_id are primary keys. If not, create indexes.

 CREATE INDEX IF NOT EXISTS relations_relation_type_idx ON origin_osm.relations (relation_type);
 CREATE INDEX IF NOT EXISTS ways_tags_idx ON origin_osm.ways USING gin(tags);
 CREATE INDEX IF NOT EXISTS relations_tags_idx ON origin_osm.relations USING gin(tags);

 -- Multipolygon Relations Materialized View (optimized)
 CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.multipolygon_relations AS
 SELECT
   r.osm_id,
   ST_BuildArea(ST_Collect(w.geometry)) AS geometry
 FROM origin_osm.relations r
 JOIN origin_osm.relation_members rm ON r.osm_id = rm.parent_id AND rm.member_type = 1
 JOIN origin_osm.ways w ON rm.osm_id = w.osm_id
 WHERE r.relation_type = 'multipolygon'
 GROUP BY r.osm_id
 WITH NO DATA;

 -- Forests Simplified Materialized View (optimized)
 CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.forests_simplified AS
 SELECT
   osm_id,
   ST_SimplifyPreserveTopology(
     CASE
       WHEN NOT ST_IsValid(geometry) THEN ST_MakeValid(geometry, 'method=structure')
       ELSE geometry
     END,
     100
   ) AS geometry,
   element_type
 FROM (
   SELECT
     w.osm_id,
     ST_BuildArea(w.geometry) AS geometry,
     1 AS element_type
   FROM origin_osm.ways w
   WHERE (w.tags ->> 'landuse') = 'forest' OR (w.tags ->> 'natural') = 'wood'
   UNION ALL
   SELECT
     r.osm_id,
     mpr.geometry,
     2 AS element_type
   FROM origin_osm.relations r
   JOIN proc_osm.multipolygon_relations mpr ON r.osm_id = mpr.osm_id
   WHERE ((r.tags ->> 'landuse') = 'forest' OR (r.tags ->> 'natural') = 'wood')
     AND r.relation_type = 'multipolygon'
 ) AS all_forests
 WHERE geometry IS NOT NULL
 WITH NO DATA;

 CREATE INDEX IF NOT EXISTS forests_simplified_geometry_idx ON proc_osm.forests_simplified USING gist(geometry);

 -- Forests Simplified With Areas Materialized View (optimized)
 CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.forests_simplified_with_areas AS
 WITH clustered_forests AS (
   SELECT
     osm_id,
     geometry,
     ST_ClusterDBSCAN(geometry, 100, 2) OVER () AS cluster_id,
     ST_Area(CAST(ST_Transform(geometry, 4326) AS geography(GEOMETRY, 4326))) AS area
   FROM proc_osm.forests_simplified
   WHERE ST_Area(geometry) > 0
 ), forest_area_for_cluster_id AS (
   SELECT
     cluster_id,
     SUM(area) AS total_area
   FROM clustered_forests
   WHERE cluster_id IS NOT NULL
   GROUP BY cluster_id
 )
 SELECT
   cf.geometry,
   cf.osm_id,
   COALESCE(fa.total_area, cf.area) AS total_area,
   cf.cluster_id
 FROM clustered_forests cf
 LEFT JOIN forest_area_for_cluster_id fa ON fa.cluster_id = cf.cluster_id
 WITH NO DATA;

 -- Relevant Forests Simplified Materialized View (optimized)
 CREATE MATERIALIZED VIEW IF NOT EXISTS proc_osm.relevant_forests_simplified AS
 SELECT
   geometry,
   osm_id,
   total_area,
   cluster_id
 FROM proc_osm.forests_simplified_with_areas
 WHERE total_area > 500000
 WITH NO DATA;
