import difflib
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Data(db.Model):
    """
    Class ``Data`` represents a table in SQL database
    """
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    left = db.Column(db.String(1000), unique=True)
    right = db.Column(db.String(1000), unique=True)

    def __init__(self, data_id, left=None, right=None):
        """
        Constructor a new ``Data`` object
        :param data_id: index of object
        :param left: "left" attribute saves base64 encoded data
        :param right: "right" attribute saves base64 encoded data
        """
        self.id = data_id
        self.left = left
        self.right = right

    @property
    def diff(self):
        """
        Return difference between right and left parameters if they exist and
        are not None, otherwise return None
        :return: difference or None 
        """
        if self.left is None or self.right is None:
            return None
        else:
            if self.left == self.right:
                return {"diff": "sides are equal"}
            elif len(self.left) != len(self.right):
                return {"diff": "sides have different size"}
            else:
                match = difflib.SequenceMatcher(
                    None, self.left, self.right).find_longest_match(
                        0, len(self.left), 0, len(self.right))
                return {"diff": "diff starts from offset %d" % match.size}

    def __repr__(self):
        """
        Representation property for ``Data`` object
        :return: representation string
        """
        return '<Data[{}] L:{} - R:{} D:{}>'.format(
            self.id,
            int(bool(self.left)),
            int(bool(self.right)),
            int(bool(self.diff)))
