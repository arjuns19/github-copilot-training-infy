from urllib.parse import quote


def test_root_redirect(client):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (301, 302, 307, 308)
    assert resp.headers.get("location") == "/static/index.html"


def test_get_activities(client):
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_remove(client):
    activity = "Chess Club"
    email = "testuser@example.com"
    path = f"/activities/{quote(activity)}/signup"

    r = client.post(path, params={"email": email})
    assert r.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # duplicate signup -> 400
    r2 = client.post(path, params={"email": email})
    assert r2.status_code == 400

    # remove
    del_path = f"/activities/{quote(activity)}/participants"
    r3 = client.delete(del_path, params={"email": email})
    assert r3.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]

    # removing again -> 404
    r4 = client.delete(del_path, params={"email": email})
    assert r4.status_code == 404


def test_signup_nonexistent(client):
    resp = client.post("/activities/NoSuchActivity/signup", params={"email":"a@b.com"})
    assert resp.status_code == 404


def test_remove_participant_not_found(client):
    resp = client.delete("/activities/Chess Club/participants", params={"email":"noone@x.com"})
    assert resp.status_code == 404
