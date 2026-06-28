#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route("/events")
def get_events():

    events = Event.query.all()

    event_list = []

    for event in events:
        event_list.append({
            "id": event.id,
            "name": event.name,
            "location": event.location
        })

    return jsonify(event_list), 200


@app.route("/events/<int:id>/sessions")
def get_event_sessions(id):

    event = Event.query.get(id)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    session_list = []

    for session in event.sessions:
        session_list.append({
            "id": session.id,
            "title": session.title,
            "start_time": session.start_time.isoformat()
        })

    return jsonify(session_list), 200


@app.route("/speakers")
def get_speakers():

    speakers = Speaker.query.all()

    speaker_list = []

    for speaker in speakers:
        speaker_list.append({
            "id": speaker.id,
            "name": speaker.name
        })

    return jsonify(speaker_list), 200


@app.route("/speakers/<int:id>")
def get_speaker(id):

    speaker = Speaker.query.get(id)

    if speaker is None:
        return jsonify({"error": "Speaker not found"}), 404

    bio = "No bio available"

    if speaker.bio:
        bio = speaker.bio.bio_text

    return jsonify({
        "id": speaker.id,
        "name": speaker.name,
        "bio_text": bio
    }), 200


@app.route("/sessions/<int:id>/speakers")
def get_session_speakers(id):

    session = Session.query.get(id)

    if session is None:
        return jsonify({"error": "Session not found"}), 404

    speaker_list = []

    for speaker in session.speakers:

        bio = "No bio available"

        if speaker.bio:
            bio = speaker.bio.bio_text

        speaker_list.append({
            "id": speaker.id,
            "name": speaker.name,
            "bio_text": bio
        })

    return jsonify(speaker_list), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)