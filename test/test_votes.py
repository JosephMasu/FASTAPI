def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post(
        "/api/v1/votes/vote",
        json={"post_id": test_posts[0].id, "dir": 1},
    )
    assert res.status_code == 201
    assert res.json().get("message") == "successfully added vote"

    listed = authorized_client.get("/api/v1/posts/sqlalchemy")
    voted = next(post for post in listed.json() if post["post"]["id"] == test_posts[0].id)
    assert voted["votes"] == 1


def test_vote_twice_post(authorized_client, test_posts):
    authorized_client.post("/api/v1/votes/vote", json={"post_id": test_posts[0].id, "dir": 1})
    res = authorized_client.post("/api/v1/votes/vote", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts):
    authorized_client.post("/api/v1/votes/vote", json={"post_id": test_posts[0].id, "dir": 1})
    res = authorized_client.post("/api/v1/votes/vote", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 201
    assert res.json().get("message") == "successfully deleted vote"


def test_delete_vote_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/api/v1/votes/vote", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, test_posts):
    res = authorized_client.post("/api/v1/votes/vote", json={"post_id": 99999, "dir": 1})
    assert res.status_code == 404


def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/api/v1/votes/vote", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401
