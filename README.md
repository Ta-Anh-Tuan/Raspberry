curl -u elastic:y0S1QpK*s4he6VIxtlbF -k -X PUT "https://localhost:9200/ELASTICSEARCH_INDEX" \
-H "Content-Type: application/json" \
-d '{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "mappings": {
    "properties": {
      "camera_id": { "type": "keyword" },
      "camera_name": { "type": "keyword" },
      "timestamp": { "type": "date" },
      "datetime": { "type": "date" },
      "img_path": { "type": "keyword" },
      "gender": { "type": "keyword" },
      "age": { "type": "keyword" },
      "vitality": { "type": "keyword" },
      "hair_color": { "type": "keyword" },
      "hair_length": { "type": "keyword" },
      "hat_color": { "type": "keyword" },
      "hat_category": { "type": "keyword" },
      "shirt_color": { "type": "keyword" },
      "shirt_category": { "type": "keyword" },
      "shirt_pattern": { "type": "keyword" },
      "shirt_sleeve_length": { "type": "keyword" },
      "pants_color": { "type": "keyword" },
      "pants_category": { "type": "keyword" },
      "pants_pattern": { "type": "keyword" },
      "shoes_color": { "type": "keyword" },
      "shoes_category": { "type": "keyword" },
      "bag_category": { "type": "keyword" },
      "bag_color": { "type": "keyword" },
      "other_category": { "type": "keyword" },
      "other_color": { "type": "keyword" },
      "rtsp_url": { "type": "keyword" }
    }
  }
}'

