from app import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/api/v1/posts/sqlalchemy")
    assert res.status_code == 200
    posts = [schemas.PostOut(**post) for post in res.json()]
    assert len(posts) == len(test_posts)
    assert {post.post.title for post in posts} == {post.title for post in test_posts}
    assert all(post.votes == 0 for post in posts)


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/api/v1/posts/sqlalchemy")
    assert res.status_code == 401


def test_get_all_posts_search(authorized_client, test_posts):
    res = authorized_client.get("/api/v1/posts/sqlalchemy", params={"search": "first"})
    assert res.status_code == 200
    posts = [schemas.PostOut(**post) for post in res.json()]
    assert len(posts) == 1
    assert posts[0].post.title == "first title"


def test_get_latest_post(client, test_posts):
    res = client.get("/api/v1/posts/latest/sqlalchemy")
    assert res.status_code == 200
    latest = schemas.PostOut(**res.json())
    assert latest.post.id == test_posts[-1].id


def test_get_latest_post_not_found(client):
    res = client.get("/api/v1/posts/latest/sqlalchemy")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/api/v1/posts/slqalchemy/{test_posts[0].id}")
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.post.id == test_posts[0].id
    assert post.post.title == test_posts[0].title


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/api/v1/posts/slqalchemy/99999")
    assert res.status_code == 404


def test_get_other_user_post(authorized_client, test_posts):
    res = authorized_client.get(f"/api/v1/posts/slqalchemy/{test_posts[3].id}")
    assert res.status_code == 403


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/api/v1/posts/slqalchemy/{test_posts[0].id}")
    assert res.status_code == 401


def test_create_post(authorized_client, test_user):
    res = authorized_client.post(
        "/api/v1/posts/sqlalchemy",
        json={"title": "new title", "content": "new content"},
    )
    assert res.status_code == 201
    created = schemas.Post(**res.json())
    assert created.title == "new title"
    assert created.content == "new content"
    assert created.owner_id == test_user["id"]
    assert created.owner.email == test_user["email"]


def test_unauthorized_user_create_post(client):
    res = client.post(
        "/api/v1/posts/sqlalchemy",
        json={"title": "new title", "content": "new content"},
    )
    assert res.status_code == 401


def test_delete_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/api/v1/posts/slqalchemy/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_posts):
    res = authorized_client.delete("/api/v1/posts/slqalchemy/99999")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/api/v1/posts/slqalchemy/{test_posts[3].id}")
    assert res.status_code == 403


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/api/v1/posts/slqalchemy/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_post(authorized_client, test_posts):
    data = {"title": "updated title", "content": "updated content"}
    res = authorized_client.put(f"/api/v1/posts/slqalchemy/{test_posts[0].id}", json=data)
    assert res.status_code == 200

    fetched = authorized_client.get(f"/api/v1/posts/slqalchemy/{test_posts[0].id}")
    updated = schemas.PostOut(**fetched.json())
    assert updated.post.title == data["title"]
    assert updated.post.content == data["content"]


def test_update_other_user_post(authorized_client, test_posts):
    data = {"title": "updated title", "content": "updated content"}
    res = authorized_client.put(f"/api/v1/posts/slqalchemy/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_update_post_non_exist(authorized_client, test_posts):
    data = {"title": "updated title", "content": "updated content"}
    res = authorized_client.put("/api/v1/posts/slqalchemy/99999", json=data)
    assert res.status_code == 404


def test_unauthorized_user_update_post(client, test_posts):
    data = {"title": "updated title", "content": "updated content"}
    res = client.put(f"/api/v1/posts/slqalchemy/{test_posts[0].id}", json=data)
    assert res.status_code == 401
