from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, ScaledFloat, Date, Search, Integer
from elasticsearch import Elasticsearch

from elasticsearch.helpers import bulk
from mswiggy import models

connections.create_connection()

es = Elasticsearch()

class UpdateLocationIndex(DocType):
	driver_id = Integer()
	driver = Text()
	lat = ScaledFloat(scaling_factor=1000)
	lon = ScaledFloat(scaling_factor=1000)
	add_time = Date()

	class Meta:
		index = 'geo'


def bulk_indexing():
	UpdateLocationIndex.init()
	bulk(client=es, actions=(b.indexing() for b in models.UpdateLocation.objects.all().iterator()))


def search(driver):
	s = Search().filter('term', driver=driver)
	response = s.execute()
	return response


def query_for_driver_search(lat1, lon1):
	response = es.search(
		index="geo",doc_type='doc',
		body={
			"from": 0, "size": 10,
			  "query": {
				"bool": {
				  "must": {
					"match_all": {}
				  },
				  "filter": {
					"geo_distance": {
					  "distance": "4km",
					  "pin": {
						"lat": lat1,
						"lon": lon1
					  }
					}
				  }
				}
			  },
			# "sort": [
			# 	{
			#
			# 			"order": "asc",
			# 		}
			#
			# ]
			})

	all_hits = response['hits']
	if all_hits['total'] != 0:
		driver_objects = all_hits['hits']
		driver_list = [i['_source'] for i in driver_objects]
		drivers = [(i['driver'], i['driver_id']) for i in driver_list]
		return drivers
	return 'No Drivers present'