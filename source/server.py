from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import psycopg2
import datetime
from database import database


def keep_alive(request):
    """
    keep_alive  process the keep alive route /keep_alive 
    :param request: 
    :return: 
    """
    if request.method == "OPTIONS":
        return  Response(status=200,  headers=cors_headers)
    else:
        return Response(status=200,  headers=cors_headers,
                        body=datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S"))


def parking_spots(request):
    if request.method == 'GET':
        params = request.params.dict_of_lists()
        lat = params['lat']
        long = params['long']
        radius = params['radius']
        cursor.execute(
            "select rows_to_json from (select * from ridecell.parking_spots where  %s < distance(%s, %s, %s, %s));",
            radius, lat, long)
        rows = cursor.fetchall()
        return Response(status=200, headers=cors_headers, json_body=rows[0][0])
    else:
        return Response(status=400, headers=cors_headers)


def reservations(request):
    if request.method == 'POST':
        json_data = request.json()
        try:
            cursor.exectute("insert into ridecell.parking_spot_reservation values (spot_id, user_id, duration values(%s, 1,'[%s,%s]  );",
                            json_data['spot_id'], json_data['start_time'], json_data['end_time'])
        except psycopg2.Error as e:
            pass
    else:
        return Response(status=400, headers=cors_headers)


cursor = None
cors_headers = {"Access-Control-Allow-Origin":  "*"}

if __name__ == '__main__':
    """
    Connect to the database
    Define the routes and supporting views
    """
    cursor = database()
    config = Configurator()
    config.add_route('keep_alive', '/keep_alive')
    config.add_view(keep_alive, route_name='keep_alive')
    config.add_route('parking_spots', '/parking_spots')
    config.add_view(parking_spots, route_name='parking_spots')
    config.add_route('reservations', '/reservations')
    config.add_view(reservations, route_name='reservations')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8081, app)
    server.serve_forever()
