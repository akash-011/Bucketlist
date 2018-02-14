from flask_restplus import reqparse

pagination_arg = reqparse.RequestParser()
pagination_arg.add_argument('page', type=int, required=False, default=1,help='Page Number')
pagination_arg.add_argument('per_page',type=int, required=False, choices=[5,10,20,25,50],default=1, help='Bucketlists per Page')
pagination_arg.add_argument('q',required=False,help='Search')
