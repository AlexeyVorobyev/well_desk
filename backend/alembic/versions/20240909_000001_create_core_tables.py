"""Create core tables for Well Desk API"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20240909_000001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_profile",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("role", sa.String(), nullable=True),
        sa.Column("work_style", sa.String(), nullable=True),
        sa.Column("work_hours_from", sa.String(), nullable=True),
        sa.Column("work_hours_to", sa.String(), nullable=True),
        sa.Column("break_interval_minutes", sa.Integer(), nullable=True),
        sa.Column("screen_break_preference", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("user_profile.id"), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("reply_to_id", sa.Integer(), sa.ForeignKey("messages.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "wellbeing",
        sa.Column("user_id", sa.String(), primary_key=True),
        sa.Column("energy", sa.Integer(), nullable=False),
        sa.Column("stress", sa.Integer(), nullable=False),
        sa.Column("focus", sa.Integer(), nullable=False),
        sa.Column("mood", sa.String(), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("wellbeing")
    op.drop_table("messages")
    op.drop_table("user_profile")
