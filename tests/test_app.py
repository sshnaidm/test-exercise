from testex import create_app
from testex.models import db, Data
import json
import os
from ddt import ddt, data
from flask_testing import TestCase


@ddt
class Test(TestCase):
    def create_app(self):
        app = create_app("config.py")
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 0
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
            os.path.dirname(__name__), 'test.db')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @data(
        [1, [1, 2, 3, 4], [1, 2, 3, 5], "diff starts from offset 3"],
        [10, [1, 2, 3], [1, 2], "sides have different size"],
        [20, [5], [6, 7], "sides have different size"],
        [100, "abcdef", "abcdef", "sides are equal"],
        [101, "", "", "sides are equal"]
    )
    def test_Mmodel(self, val):
        num, left, right, expected = val
        d = Data(num)
        d.left, d.right = left, right
        diff = d.diff
        self.assertIsNotNone(diff)
        self.assertIn("diff", diff, "Diff doesn't have data")
        self.assertEqual(
            diff["diff"], expected,
            "right is %s and left is %s and diff is wrong %s" % (
                str(d.right), str(d.left), str(d.diff["diff"])))

    @data(
        [1, None, None, None],
        [10, None, "right", None],
        [20, "left", None, None],

    )
    def test_Model2(self, val):
        num, left, right, expected = val
        d = Data(num)
        d.left, d.right = left, right
        diff = d.diff
        self.assertEqual(
            diff, expected,
            "right is %s and left is %s and diff is wrong %s" % (
                str(d.right), str(d.left), str(d.diff)))

    @data(
        [10, "abcdef", "abcdef", "sides are equal"],
        [1, "123456", "123890", "diff starts from offset 3"],
        [10, "aaa", "aa", "sides have different size"],
        [20, "", "12345", "sides have different size"],
    )
    def test_DBModel(self, val):
        num, left, right, expected = val
        d = Data(num)
        d.left, d.right = left, right
        db.session.add(d)
        db.session.commit()
        db_d = Data.query.get(num)
        diff = db_d.diff
        self.assertIsNotNone(diff)
        self.assertIn("diff", diff, "Diff doesn't have data")
        self.assertEqual(
            diff["diff"], expected,
            "right is %s and left is %s and diff is wrong %s" % (
                str(d.right), str(d.left), str(d.diff)))

    @data(
        [1, None, None, None],
        [10, None, "right", None],
        [20, "left", None, None],
    )
    def test_DBModel2(self, val):
        num, left, right, expected = val
        d = Data(num)
        d.left, d.right = left, right
        db.session.add(d)
        db.session.commit()
        db_d = Data.query.get(num)
        diff = db_d.diff
        self.assertIsNone(diff)
        self.assertEqual(
            diff, expected,
            "right is %s and left is %s and diff is wrong %s" % (
                str(d.right), str(d.left), str(d.diff)))

    def test_server(self):
        response = self.client.get("/")
        self.assertEqual(response.data, b'Welcome')

    @data(
        ["/v1/diff/7/left", "fake", 400],
        ["/v1/diff/6/right", "", 400],
        ["/v1/diff/-1/right", "string", 404],
        ["/v1/diff/5/right", b'bytes', 400],
        ["/v1/diff/5/wrong", "str", 404],
        ["/v1/diff/5", "fake", 405],
        ["/v1/diff", "fake", 404],
        ["/v1", "fake", 404],
    )
    def test_api_negative(self, val):
        url, data, code = val
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, code)

    @data(
        ["/v1/diff/7/left", {}, 400],
        ["/v1/diff/5/right", {"nodata": ""}, 400],
        ["/v1/diff/7/left", {"data": ""}, 400],
        ["/v1/diff/5/right", {"data": "", "nodata": ""}, 400],
        ["/v1/diff/7/left", {"data": "string"}, 400],
        ["/v1/diff/5/right", {"data": 100}, 400],
        ["/v1/diff/7/left", {"data": [1, 2]}, 400],
        ["/v1/diff/15/right", {
            "data": "Ynl0ZXM="}, 400],
    )
    def test_api_post_data(self, val):
        url, js, code = val
        data = json.dumps(js)
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, code)

    @data(
        ["/v1/diff/18/left", {"data": "Ynl0ZXo="}, 200],
        ["/v1/diff/20/right", {"data": "Ynl0ZXM="}, 200],
        ["/v1/diff/1/left", {"data": "notbinary"}, 400],
        ["/v1/diff/2/right", {"data": "some_string"}, 400],
    )
    def test_api_json(self, val):
        url, js, code = val
        data = json.dumps(js)
        response = self.client.post(
            url,
            data=data,
            content_type='application/json')
        self.assertEqual(response.status_code, code)

    @data(
        [42, "Ynl0ZXo=", "Ynl0ZXM=", 200, "diff starts from offset 6"],
        [43, "Ynl0ZXo=", "Ynl0ZXMxMjM=", 200, "sides have different size"],
        [43, "Ynl0ZXMxMjM=", "Ynl0ZXo=", 200, "sides have different size"],
        [43, "Ynl0ZXo=", "Ynl0ZXo=", 200, "sides are equal"],
    )
    def test_api_e2e(self, val):
        with self.create_app().app_context():
            num, l, r, code, result = val
            left = json.dumps({"data": l})
            right = json.dumps({"data": r})

            response = self.client.post(
                "/v1/diff/%d/left" % num,
                data=left,
                content_type='application/json')
            self.assertEqual(response.status_code, code)
            response = self.client.post(
                "/v1/diff/%d/right" % num,
                data=right,
                content_type='application/json')
            self.assertEqual(response.status_code, code)
            response = self.client.get("/v1/diff/%d" % num)
            self.assertEqual(response.json['diff'], result, response.data)
