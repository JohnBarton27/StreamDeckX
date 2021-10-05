import logging
import sqlite3 as sl

from dao.dao import Dao


class ActionDao(Dao):

    def get_by_id(self, action_id: int, button=None):
        """
        Given an action ID, returns that Action object

        Args:
            action_id (int): Database ID of the action
            button (Button): Button that this action belongs to [optional]. If not given, will pull from the database using a separate query.

        Returns:
            Action: action object
        """
        conn = ActionDao.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM action WHERE id=?;
            """, (str(action_id),))

            result = cursor.fetchall()
            if not result:
                return None

        button = ActionDao.get_obj_from_result(dict(result[0]), button=button)
        return button

    def get_for_button(self, button):
        """
        Given a Button object, get all Actions that are assigned to this Button

        Args:
            button (Button): Button object to get all the Actions for

        Returns:
            Action[]: List of Action objects
        """
        conn = ActionDao.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM action WHERE button_id=?;
            """, (str(button.id),))

            results = cursor.fetchall()
            if not results:
                return None

        actions = ActionDao.get_objs_from_result(results, button=button)
        return actions

    def create(self, action):
        """
        Creates the given Action object in the database.

        Args:
            action (Action): Action object to insert into the database

        Returns:
            None
        """
        conn = ActionDao.get_db_conn()

        with conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT into action (type, button_id, action_order, parameter) VALUES (?, ?, ?, ?);
            """, (action.action_type, action.button.id, action.order, action.parameter))
            conn.commit()

    def update(self, action):
        """
        Updates the given Action in the database

        Args:
            action (Action): Action object that already exists in the database, but may need updating

        Returns:
            None
        """
        conn = ActionDao.get_db_conn()

        with conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE action SET action_order = ?, parameter = ? WHERE id = ?;
            """, (action.order, action.parameter, action.id))
            logging.info(
                f'Updating action ({action.id}): order = {action.order} | parameter = {action.parameter}')
            conn.commit()

    @staticmethod
    def get_obj_from_result(result, button=None):
        """
        Given a single SQL result containing a single action, get the Action object represented by this result.

        Args:
            result (dict): SQL result containing a single action
            button (Button): Button object this action belongs to - if not given, will use a separate DB query to populate

        Returns:
            Action: Action object represented by the SQL result
        """
        from action import ActionFactory

        action_id = result['id']
        action_type = result['type']
        button_id = result['button_id']
        action_order = result['action_order']
        parameter = result['parameter']

        if not button:
            from dao.button_dao import ButtonDao
            button_dao = ButtonDao()
            button = button_dao.get_by_id(button_id)

        action_class = ActionFactory.get_by_type(action_type)
        action = action_class(parameter, button, action_order, action_id=action_id)
        return action

    @staticmethod
    def get_objs_from_result(results, button=None):
        """
        Given a set of SQL results (which may contain multiple rows, each corresponding to a different action on the same Button), get the Action objects that are represented by the SQL results.

        Args:
            results (list): List of SQL rows that each contain an Action, all on the same Button
            button (Button): Button that all the actions belong to. If not given, will be populated.

        Returns:
            Action[]: List of Action objects
        """
        actions = []

        for result in results:

            if not button:
                # Setup 'button' once
                from dao.button_dao import ButtonDao
                button_dao = ButtonDao()
                button_id = result['button_id']
                button = button_dao.get_by_id(button_id)

            actions.append(ActionDao.get_obj_from_result(dict(result), button=button))

        return actions
