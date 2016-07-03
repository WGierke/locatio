#! /usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, request, send_from_directory, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Shipment


@app.route('/')
def index():
    s = Shipment.query.all()
    return render_template("index.html", shipments=s)

@app.route('/overview/<int:id>')
def overview(id):
    shipments = Shipment.query.filter_by(id=id).all()
    if len(shipments) >= 1:
        s = shipments[0]
    else:
        return 404
    return render_template("shipmentOverview.html", shipment=s)

@app.route('/newRoute')
def newRoute():
    return render_template("newRoute.html")

@app.route('/get_closests/<int:id>')
def get_closests(id):
    s = Shipment.query.filter_by(id=id)
    return jsonify(s.find_closests_shipments())

@app.route('/shipment/<int:id>')
def get_shipment(id):
    s = Shipment.query.filter_by(id=id).all()
    if s:
        d = {"id": id, "lat": s[0].get_end_location().lat, "lng": s[0].get_end_location().lng}
        return jsonify(d)
    return 404

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory("static/js", path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory("static/images", path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory("static/css", path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory("static/fonts", path)

@app.route('/font/<path:path>')
def send_font(path):
    return send_from_directory("static/font", path)

@app.route('/node_modules/<path:path>')
def send_node_modules(path):
    return send_from_directory("static/node-modues", path)

if __name__ == '__main__':
    app.run()
