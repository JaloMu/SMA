from flask import render_template, request, redirect, url_for
from app.utils import req_m, test_print
from os.path import dirname
from . import dns
from ..models.DNS import DNS, Zones
from .. import db
from flask_login import login_required
from datetime import datetime


team = dirname(__file__).split("/")[-1]


@dns.route('/dns_list', methods=["GET", "POST"])
@login_required
def dns_list():
    zones = Zones.query.all()
    hosts = DNS.query.all()
    if not zones:
        return redirect(request.args.get("next") or url_for('.zone_add'))
    if (req_m(request) == 1):
        return render_template('sdns/dns_list.html',zones=zones,hosts=hosts)
    return render_template('sdns/dns_list.html', zones=zones,hosts=hosts)


@dns.route('/dns_add', methods=["GET", "POST"])
@login_required
def dns_add():
    dns = DNS()
    error = None
    msg = None
    ns = DNS.query.filter_by(zone_id=request.args.get("id")).first()
    nowTime = datetime.now().strftime('%Y%m%d%H%M%S')
    dns.serial=nowTime
    zonename = request.args.get("zonename")
    dns.zone_id = request.args.get("id")
    hosts = db.session.query(DNS.host).filter(DNS.zone_id==dns.zone_id).all()
    dns.resp_person = '{}.{}.'.format('root',zonename)
    dns.primary_ns = ns.primary_ns
    if (req_m(request) == 1):
        if (request.form.get("host"),) in hosts:
            return render_template('sdns/host_add.html', nowTime=nowTime, zonename=zonename, error="主机名重复")
        for k, v in request.form.items():
            setattr(dns, k, v)
        db.session.add(dns)
        db.session.commit()
        return render_template('sdns/host_add.html', nowTime=nowTime, zonename=zonename,msg="添加成功")
    return render_template('sdns/host_add.html',nowTime=nowTime,zonename=zonename)


@dns.route('/dns_edit', methods=["GET", "POST"])
@login_required
def dns_edit():
    flag = 0
    id = request.args.get("id")
    dns = DNS.query.filter_by(id=id).first()
    test_print(request.form)
    if (req_m(request) == 1):
        for k, v in request.form.items():
            if k == "zone_id":
                continue
            if v != getattr(dns, k):
                setattr(dns, k, v)
                flag = 1
        if flag == 1:
            nowTime = datetime.now().strftime('%Y%m%d%H%M%S')
            dns.serial = nowTime
            db.session.add(dns)
            db.session.commit()
            return redirect(request.args.get("next") or url_for('.dns_list'))
        return render_template('sdns/dns_edit.html', dns=dns)
    return render_template('sdns/dns_edit.html', dns=dns)


########################################################################################################################
@dns.route('/zone_add', methods=["GET", "POST"])
@login_required
def zone_add():
    zones = set(db.session.query(DNS.zone).all())
    hosts = DNS.query.all()
    error = None
    msg = None
    if (req_m(request) == 1):
        zone = Zones()
        if request.form.get('zone') == '':
            error =  '失败'
            return render_template('sdns/zone_add.html',error=error)
        zone.zone = request.form.get('zone')
        test_print(zone.zone)
        db.session.add(zone)
        db.session.commit()
        dns = DNS()
        if request.form.get("primary_ns") == '':
            dns.primary_ns = '{}.{}.'.format('ns',zone.zone)
            dns.data = dns.primary_ns
        else:
            dns.primary_ns = '{}.{}.'.format(request.form.get("primary_ns"), zone.zone)
            dns.data = dns.primary_ns
        dns.zone_id = zone.id
        dns.type = 'SOA'
        dns.resp_person = '{}.{}.'.format('root',zone.zone)
        db.session.add(dns)
        db.session.commit()
        msg = '添加 {} 成功'.format(zone.zone)
        return render_template('sdns/zone_add.html', msg=msg)
    return render_template('sdns/zone_add.html')