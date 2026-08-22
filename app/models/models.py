from app.db.dbsession import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import func, ForeignKey


# Пользователи
class Users(Base):
    __tablename__ = 'users'
    id : Mapped [int] = mapped_column(primary_key=True)
    user_name : Mapped[str] = mapped_column(nullable=False)
    second_name : Mapped[str] = mapped_column(nullable=True)
    patronymic : Mapped[str] = mapped_column(nullable=True)
    email : Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash : Mapped[str] = mapped_column(nullable=False)
    is_active : Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at : Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at : Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False,)

    role_id : Mapped[int] = mapped_column(ForeignKey('role.id', ondelete='SET NULL' ), nullable=True)
    role = relationship('Role', back_populates='users')


# Роли
class Role(Base):
    __tablename__ = 'role'
    id: Mapped[int] = mapped_column(primary_key=True)
    role_name : Mapped[str]=mapped_column(unique=True)

    permissions = relationship("Permissions", secondary="rolePermissions", back_populates="roles")
    users = relationship('Users', back_populates='role')


# Права на действия
class Permissions(Base):
    __tablename__ = 'permissions'
    id:Mapped[int] = mapped_column(primary_key=True)
    codename:Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()

    roles = relationship("Role", secondary="rolePermissions", back_populates="permissions")


# Связь Role с Permissions
class RolePermissions(Base):
    __tablename__ = 'rolePermissions'
    id: Mapped[int] = mapped_column(primary_key=True)
    role_id : Mapped[int]=mapped_column(ForeignKey("role.id", ondelete='CASCADE'))
    permission_id : Mapped[int]=mapped_column(ForeignKey("permissions.id", ondelete='CASCADE'))






