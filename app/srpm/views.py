from flask import render_template, request, jsonify
from . import srpm
from app.utils import req_m, test_print
from os.path import dirname
from flask_login import login_required
import yaml


team = dirname(__file__).split("/")[-1]


@srpm.route('/make', methods=["GET", "POST"])
@login_required
def make():
    cmd = {}
    if (req_m(request) ==1):
        test_print(yaml.dump(request.form.to_dict(), indent=4, default_flow_style=False))
        # rpmCmd = "fpm -f -s dir -t {typt} -n {rpmname} -v {version} --iteration {release} -C / --epoch 0 -p  \
        # --rpm-user {user} --rpm-group {group} -d '{depends}' --no-auto-depends --verbose \
        # --before-install {install_before} --after-install \
        # --before-remove {remove_before} --after-remove remove_after --directories {files}".format_map(cmd)
        # test_print(rpmCmd)
        return render_template("rpm/rpmFactory.html")
    return render_template("rpm/rpmFactory.html")