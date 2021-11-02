# OPTIONAL Wave 3: Enhancements & Deployment

These really are **optional** - if you've gotten here and you have time left, that means you're moving speedy fast!

## Enhancements

### Query Parameters
Any endpoint that returns a list should accept 3 _optional_ query parameters:

| Name   | Value   | Description
|--------|---------|------------
| `sort` | string  | Sort objects by this field, in ascending order
| `n`    | integer | Number of responses to return per page
| `p`    | integer | Page of responses to return

So, for an API endpoint like `GET /customers`, the following requests should be valid:
- `GET /customers`: All customers, sorted by ID
- `GET /customers?sort=name`: All customers, sorted by name
- `GET /customers?n=10&p=2`: Customers 11-20, sorted by ID
- `GET /customers?sort=name&n=10&p=2`: Customers 11-20, sorted by name

Things to note:
- Possible sort fields:
  - Customers can be sorted by `name`, `registered_at` and `postal_code`
  - Videos can be sorted by `title` and `release_date`
  - Overdue rentals can be sorted by `title`, `name`, `checkout_date` and `due_date`
- If the client requests both sorting and pagination, pagination should be relative to the sorted order
- Check out the [paginate method](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery.paginate)

### More Endpoints: Inventory Management
All these endpoints should support all 3 query parameters. All fields are sortable.

#### `GET /rentals/overdue`
List all customers with overdue videos

Fields to return:
- `video_id`
- `title`
- `customer_id`
- `name`
- `postal_code`
- `checkout_date`
- `due_date`


#### `GET /videos/<id>/history`
List customers that have checked out a copy of the video _in the past_

URI parameters:
- `id`: Video identifier

Fields to return:
- `customer_id`
- `name`
- `postal_code`
- `checkout_date`
- `due_date`


#### `GET /customers/<id>/history`
List the videos a customer has checked out _in the past_

URI parameters:
- `id`: Customer ID

Fields to return:
- `title`
- `checkout_date`
- `due_date`

## Deployment

Consider deploying your API to Heroku following the instructions from Learn and Task List.  


## CLI

Create a Command Line Interface (CLI) program as a client for the Retro Video Store API.