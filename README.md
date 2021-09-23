# Metrics API

To start app with docker-compose:
```
make dev
```

To run tests (after running app with previous command):
```
make tests
```
Or to run a specific test:
```
make custom-tests TEST_PATH=tests/users_connected/realtime/infrastructure/test_users_connected_controller.py::test_users_in_user_connection_checker_service_are_not_connected
```

## Testing

- A sample call for the `realtime` endpoint:

```
curl -v http://localhost/connected/realtime/sperez4mba/ClojureFriends
```
which returns a response:
```
{
  "errors": [
    "ClojureFriends is not a valid user in github"
  ]
}
```
the above call doesn't register anything since ClojureFriends handle doesn't identify a valid Github user.

- A sample call for the `register` endpoint:

```
curl -v http://localhost/connected/register/sperez4mba/ClojureFriends
```
which returns an empty response because ClojureFriends handle not identifying a valid Github user:
```
{
  "data": []
}
```