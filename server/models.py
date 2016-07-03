#! /usr/bin/python
# -*- coding: utf-8 -*-

import math
from flask.ext.admin.contrib.sqla import ModelView

from app import db, admin

start_locations = db.Table('shipment_starts',
                           db.Column("shipment_id", db.Integer(), db.ForeignKey('shipments.id')),
                           db.Column("address_id", db.Integer(), db.ForeignKey('addresses.id')))

end_locations = db.Table('shipment_ends',
                         db.Column("shipment_id", db.Integer(), db.ForeignKey('shipments.id')),
                         db.Column("address_id", db.Integer(), db.ForeignKey('addresses.id')))


class Shipment(db.Model):
    __tablename__ = 'shipments'

    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.String)
    start_location_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))
    end_location_id = db.Column(db.Integer, db.ForeignKey("addresses.id"))

    pickup_name = db.Column(db.String)
    drop_off_name = db.Column(db.String)

    location_type = db.Column(db.String)

    start_locations = db.relationship('Address', secondary='shipment_starts')

    end_locations = db.relationship("Address", secondary='shipment_ends')

    def find_closest_shipments(self, n=5, max_distance=250):
        shipments = Shipment.query.filter_by(due_date=self.due_date).all()
        closest_shipments = []
        for shipment in shipments:
            if not shipment == self and shipment.get_start_location() == self.get_start_location():
                distance = self.get_end_location().distance_to(shipment.get_end_location())
                if distance < max_distance:
                    closest_shipments.append((distance, shipment))


        closest_shipments = sorted(closest_shipments, key=lambda x: x[0], reverse=False)
        if len(closest_shipments) <= n:
            return closest_shipments
        return closest_shipments[:5]

    def get_start_location(self):
        if self.start_locations:
            return self.start_locations[0]
        return EmptyLocation()

    def get_end_location(self):
        if self.end_locations:
            return self.end_locations[0]
        return EmptyLocation()


class Address(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    street = db.Column(db.String)
    street_addition = db.Column(db.String)
    postal_code = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    country = db.Column(db.String)
    location_type = db.Column(db.String)
    lat = db.Column(db.String)
    lng = db.Column(db.String)
    standard_opening_times = db.Column(db.String)
    building_type = db.Column(db.String)
    time_zone = db.Column(db.String)
    access_notes = db.Column(db.String)

    def distance_to(self, other):
        try:
            lat1 = float(self.lat)
            lat2 = float(other.lat)
            lng1 = float(self.lng)
            lng2 = float(other.lng)

            earthRadius = 6371000
            dLat = math.radians(lat2 - lat1)
            dLng = math.radians(lng2 - lng1)
            a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
                                                          math.sin(dLng / 2) * math.sin(dLng / 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            return earthRadius * c
        except:
            return 9999999

    def __repr__(self):
        s = u"{} {} {}".format(self.street if self.street else "",
                              self.postal_code if self.postal_code else "",
                              self.city if self.city else "")
        return s


class EmptyLocation:
    street = "-"
    def __repr__(self):
        return "-"

admin.add_view(ModelView(Shipment, db.session))
admin.add_view(ModelView(Address, db.session))

def load_csv_into_database(fp="../data/cleaned_and_normalized_1.csv"):
    import csv
    with open(fp) as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        for row in reader:
            if row[0] == "name":
                continue
            a = Address(name=u(row[0]), street=u(row[1]), street_addition=u(row[2]), postal_code=u(row[3]),
                        city=u(row[4]), state=u(row[5]), country=u(row[6]), location_type=u(row[7]), lat=u(row[8]),
                        lng=u(row[9]), standard_opening_times=u(row[10]), building_type=u(row[11]),
                        time_zone=u(row[12]), access_notes=u(row[13]))
            db.session.add(a)
            db.session.commit()

def u(x):
    return unicode(x, 'utf-8', 'ignore')