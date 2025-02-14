from sqlalchemy import (
    BIGINT,
    Column,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    Date,
    DateTime,
    BigInteger,
    Boolean,
    Time,
    TIMESTAMP,
    JSON
)
from database import Base
from sqlalchemy.orm import relationship


# class Tasks(Base):
#     __tablename__ = "tasks"

#     # Primary and Foreign Keys
#     id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
#     ai_project_detail_id = Column(Integer, nullable=False)
#     workflow_id = Column(Integer, nullable=False)
#     category_id = Column(BigInteger, nullable=True)

#     # Basic Task Information
#     uuid = Column(String(250), nullable=True)
#     title = Column(String(255), nullable=False)
#     description = Column(Text, nullable=True)
#     start_date = Column(Date, nullable=True)
#     video_file = Column(String(255), nullable=True)
#     completion_date = Column(Date, nullable=True)
#     reoccurring = Column(String(255), nullable=True)

#     # Agent Related Fields
#     assign_task_agent_id = Column(String(1000), nullable=True)
#     agent_tool = Column(String(1000), nullable=True)
#     agent_instruction = Column(Text, nullable=True)
#     agent_output = Column(Text, nullable=True)
#     agent_parameter = Column(Text, nullable=True)

#     # Team Member Related Fields
#     assign_task_team_member_id = Column(String(1000), nullable=True)
#     team_member_ai_agent_for_assistance = Column(String(1000), nullable=True)
#     team_member_instruction = Column(Text, nullable=True)
#     team_member_output = Column(Text, nullable=True)

#     # Colabi Member Related Fields
#     assign_task_colabi_member_id = Column(String(1000), nullable=True)
#     colabi_member_ai_agent_for_assistance = Column(String(1000), nullable=True)
#     colabi_member_instruction = Column(Text, nullable=True)
#     colabi_member_output = Column(Text, nullable=True)

#     # Self Related Fields
#     assign_task_my_self_id = Column(String(1000), nullable=True)
#     my_self_ai_agent_for_assistance = Column(String(1000), nullable=True)
#     my_self_instruction = Column(Text, nullable=True)
#     my_self_output = Column(Text, nullable=True)

#     # Client Related Fields
#     assign_task_client_id = Column(String(1000), nullable=True)
#     client_ai_agent_for_assistance = Column(String(1000), nullable=True)
#     client_instruction = Column(Text, nullable=True)
#     client_output = Column(Text, nullable=True)
#     status = Column(String(255), default=None)
#     # Metadata
#     created_at = Column(DateTime, nullable=True)
#     updated_at = Column(DateTime, nullable=True)
#     created_by = Column(Integer, nullable=False)


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    parent_task_id = Column(Integer, nullable=True)
    job_id = Column(Integer, nullable=True)
    workflow_id = Column(Integer, nullable=False)
    task_arrange = Column(Integer, default=0, nullable=False)
    category_id = Column(BigInteger, nullable=True)
    uuid = Column(String(250), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_date_time = Column(TIMESTAMP, nullable=True)
    video_file = Column(String(255), nullable=True)
    end_date_time = Column(TIMESTAMP, nullable=True)
    product_task_id = Column(BigInteger, ForeignKey('product_tasks.id', ondelete='CASCADE'), nullable=True)
    assign_task_agent_id = Column(String(1000), nullable=True)
    ai_project_detail_id = Column(Integer, nullable=True)
    agent_tool = Column(String(1000), nullable=True)
    agent_instruction = Column(Text, nullable=True)
    agent_output = Column(Text, nullable=True)
    agent_parameter = Column(Text, nullable=True)
    assign_task_team_member_id = Column(String(1000), nullable=True)
    team_member_ai_agent_for_assistance = Column(String(1000), nullable=True)
    team_member_instruction = Column(Text, nullable=True)
    team_member_output = Column(Text, nullable=True)
    assign_task_colabi_member_id = Column(String(1000), nullable=True)
    colabi_member_ai_agent_for_assistance = Column(String(1000), nullable=True)
    colabi_member_instruction = Column(Text, nullable=True)
    colabi_member_output = Column(Text, nullable=True)
    assign_task_my_self_id = Column(String(1000), nullable=True)
    my_self_ai_agent_for_assistance = Column(String(1000), nullable=True)
    my_self_instruction = Column(Text, nullable=True)
    my_self_output = Column(Text, nullable=True)
    assign_task_client_id = Column(String(1000), nullable=True)
    client_ai_agent_for_assistance = Column(String(1000), nullable=True)
    client_instruction = Column(Text, nullable=True)
    client_output = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    created_by = Column(Integer, nullable=False)
    status = Column(Integer, default=0, nullable=False, comment='0-pending, 1-completed, 2-reassigned')
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    custom_fields = Column(JSON, nullable=True)
    assign_to = Column(String(255), nullable=True)
    prev_output_checkbox = Column(String(255), nullable=True)
    paid_status = Column(Integer, default=0, nullable=False)


class CompletedTaskDetailFiles(Base):
    __tablename__ = "completed_task_detail_files"

    # Primary and Foreign Keys
    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    completed_task_detail_id = Column(Integer, nullable=False)

    # File Information
    file_name = Column(Text, nullable=False)

    # Timestamps
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class CompletedTaskDetails(Base):
    __tablename__ = "completed_task_details"

    # Primary and Foreign Keys
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    task_id = Column(Integer, nullable=False)

    # User Information
    from_user = Column(Integer, nullable=False)
    to_user = Column(Integer, nullable=False)
    from_user_role_id = Column(Integer, nullable=False)

    # Task Details
    output = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    reason_for_reassign = Column(Text, nullable=True)
    # Status Fields
    status = Column(
        SmallInteger, nullable=False, default=0
    )  # 0 => pending, 1 => completed, 2 => failed
    mark_as = Column(
        SmallInteger, nullable=False, default=0
    )  # 0 => pending, 1 => completed, 2 => reassign

    # Timestamps
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)


class WorkFlow(Base):
    __tablename__ = "work_flows"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(255), unique=True, nullable=False)
    ai_project_detail_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    start_time = Column(Time, nullable=True)
    due_date = Column(Date, nullable=True)
    app = Column(String(255), nullable=True)
    trigger = Column(String(255), nullable=True)
    prompt = Column(Text, nullable=True)
    ai_agent_ids = Column(String(255), nullable=True)
    instruction = Column(Text, nullable=True)
    created_by = Column(Integer, nullable=True)
    total_payout = Column(Integer, nullable=True)
    in_draft_step = Column(Boolean, nullable=False, default=True)
    is_completed = Column(Boolean, nullable=False, default=False)
    in_draft = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    reoccurring = Column(String(255), nullable=True)
    last_cron_run_at = Column(DateTime, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(36), nullable=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    role_id = Column(Integer, nullable=False, default=2)
    type = Column(String(255), nullable=True)
    role_type_id = Column(Integer, nullable=True)
    country_id = Column(Integer, nullable=False, default=1)
    email_verified_at = Column(DateTime, nullable=True)
    password = Column(String(255), nullable=False)
    remember_token = Column(String(100), nullable=True)
    avatar = Column(String(255), nullable=False, default="avatar.png")
    video = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    tag_line = Column(String(255), nullable=True)
    about_you = Column(Text, nullable=True)
    incentive_type = Column(String(255), nullable=True)
    incentive_comments = Column(Text, nullable=True)
    interest_comments = Column(Text, nullable=True)
    messenger_color = Column(String(255), nullable=False, default="#2180f3")
    layout = Column(String(255), nullable=True)
    business_type = Column(String(255), nullable=True)
    user_type = Column(String(255), nullable=True)
    dark_mode = Column(Boolean, nullable=False, default=False)
    active_status = Column(Boolean, nullable=False, default=True)
    lang = Column(String(255), nullable=True)
    social_type = Column(String(255), nullable=True)
    created_by = Column(BigInteger, nullable=True)
    plan_id = Column(BigInteger, nullable=True)
    plan_expired_date = Column(DateTime, nullable=True)
    phone = Column(String(255), nullable=True)
    phone_verified_at = Column(DateTime, nullable=True)
    dark_layout = Column(Boolean, nullable=False, default=False)
    rtl_layout = Column(Boolean, nullable=False, default=False)
    transprent_layout = Column(Boolean, nullable=False, default=True)
    theme_color = Column(String(255), nullable=False, default="theme-2")
    users_grid_view = Column(Boolean, nullable=False, default=False)
    forms_grid_view = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    company_name = Column(String(255), nullable=True)
    position = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    zip_code = Column(String(255), nullable=True)
    client = Column(Boolean, nullable=False, default=False)
    age = Column(String(255), nullable=True)
    gender = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    focus_group = Column(Boolean, nullable=True, default=False)
    city = Column(String(50), nullable=True)
    interests = Column(Text, nullable=True)
    interested_rate = Column(Integer, nullable=True)
    credential_send = Column(Boolean, nullable=False, default=False)
    business_name = Column(String(255), nullable=True)
    competition_value = Column(String(255), nullable=True)
    my_team = Column(Boolean, nullable=False, default=False)
    from_public = Column(Boolean, nullable=False, default=False)
    job_connected = Column(String(255), nullable=True)
    first_name = Column(String(50), nullable=True)
    gmail = Column(String(255), nullable=True)
    facebook = Column(String(255), nullable=True)
    twitter = Column(String(255), nullable=True)
    linkedIn = Column(String(255), nullable=True)
    website_name = Column(String(255), nullable=True)
    work_phone = Column(String(255), nullable=True)
    social_provider_name = Column(String(255), nullable=True)
    industry = Column(String(255), nullable=True)
    objective = Column(Text, nullable=True)
    suburb = Column(Text, nullable=True)
    group_id = Column(Text, nullable=True)
    profile_img = Column(Text, nullable=True)
    profile_overview = Column(Text, nullable=True)
    subscription_id = Column(String(255), nullable=True)
    wordpress_uid = Column(String(255), nullable=True)
    wordpress_lid = Column(String(255), nullable=True)
    profile_status = Column(
        Boolean, nullable=False, default=False, comment="0 => Public, 1 => Private"
    )
    stripe_customer_id = Column(String(255), nullable=True)
    previous_role_id = Column(Integer, nullable=True)
    admin_respondent = Column(Boolean, nullable=False, default=False)


class TaskUser(Base):
    __tablename__ = "task_user"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    task_id = Column(
        BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    user_type = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)

    # Optional: Add relationships to users and tasks models if they exist
    # user = relationship("User", back_populates="task_users")
    # task = relationship("Task", back_populates="task_users")
