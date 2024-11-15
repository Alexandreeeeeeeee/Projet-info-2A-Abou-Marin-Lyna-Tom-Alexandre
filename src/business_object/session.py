class Session:
    """Classe pour représenter une session utilisateur."""

    def __init__(self, session_id, ts, auth, level, user_agent, item_in_session, user_id_id):
        """
        Initialise une nouvelle instance de la classe Session.

        :param session_id: ID de la session.
        :param ts: Timestamp de la session.
        :param auth: Type d'authentification utilisé pour la session.
        :param level: Niveau d'accès de l'utilisateur pour la session.
        :param user_agent: Agent utilisateur de l'appareil utilisé pour la session.
        :param item_in_session: Identifiant d'un élément spécifique dans la session.
        :param user_id_id: ID de l'utilisateur auquel la session est associée.
        """
        self.session_id = session_id
        self.ts = ts
        self.auth = auth
        self.level = level
        self.user_agent = user_agent
        self.item_in_session = item_in_session
        self.user_id_id = user_id_id

    def __repr__(self):
        """Retourne une représentation en chaîne de caractères de la session."""
        return (
            f"Session(session_id={self.session_id}, ts={self.ts}, auth='{self.auth}', "
            f"level='{self.level}', user_agent='{self.user_agent}', "
            f"item_in_session={self.item_in_session}, user_id_id={self.user_id_id})"
        )
