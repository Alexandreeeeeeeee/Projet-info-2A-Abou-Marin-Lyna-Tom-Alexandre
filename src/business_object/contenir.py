"""
Module contenant la classe Contenir, qui représente la relation entre une session et une chanson.
"""

class Contenir:
    """Classe pour représenter le lien entre une session et une chanson."""

    def __init__(self, identifier, session_id, song_id):
        """
        Initialise une nouvelle instance de la classe Contenir.

        :param identifier: ID unique pour la relation (auto-incrément).
        :param session_id: ID de la session associée.
        :param song_id: ID de la chanson associée.
        """
        self.identifier = identifier
        self.session_id = session_id
        self.song_id = song_id

    def __repr__(self):
        """Retourne une représentation en chaîne de caractères de l'objet Contenir."""
        return (
            f"Contenir(identifier={self.identifier}, "
            f"session_id={self.session_id}, song_id={self.song_id})"
        )
