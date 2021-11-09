from sqlalchemy.orm import Session
from .model import User
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


class UserInfo:

    def __init__(self, config: dict, user_id: int):
        """
        This is a class grouping all the relevant attributes from user config file to make the purchase.
        :param config: The user_config file from the postgres.
        :param user_id: the id of the user.
        """
        self.user_id = user_id
        self._logger = logger
        self._is_valid = True

        try:
            self._username = config['username']
            self._password = config['password']
            self._email = config['email']
            self._purchases = config['purchases']
        except KeyError as e:
            self._logger.error(f"a key is missing this is incorrect {e}")
            self._is_valid = False

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def email(self):
        return self._email

    @property
    def purchases(self):
        return self._purchases

    @property
    def is_valid(self):
        return self._is_valid

    @property
    def credentials(self):
        return {
            "email": self._email,
            "password": self._password
        }

    def update_purchase(self, session: Session, product_id: int):
        """
        This method updates the database with the latest purchase
        :param session: the Session object with the database connection.
        :param product_id: the product_id that has been purchased.
        :return: None
        """
        try:
            row = session.query(User).filter(User.id == self.user_id).one_or_none()
            if row.config['purchases'] is None:
                row.config['purchases'] = [product_id]
            else:
                row.config['purchases'].append(product_id)
            session.add(row)
            session.flush()
        except SQLAlchemyError as e:
            self._logger.error(f"ORM error: {e}")
            self._is_valid = False
            session.rollback()
        finally:
            session.close()
