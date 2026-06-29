from flask import Blueprint, render_template
from flask_login import current_user, login_required

from ..models import User

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
@login_required
def me():
    return render_template("profile.html", user=current_user, own=True)


@profile_bp.route("/profile/<int:user_id>")
@login_required
def view(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("profile.html", user=user, own=(user.id == current_user.id))
