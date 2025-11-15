#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Db > Mission
#
from typing import List
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.sql import func

from lib.db.Session import Base
from lib.db.Host import Host


class Mission(Base):
    __tablename__ = 'missions'

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(255), nullable=False, default='')
    comment: Mapped[str] = Column(String(255), nullable=False, default='')
    creation_date: Mapped[DateTime] = Column(DateTime, default=func.now())

    hosts: Mapped[List["Host"]] = relationship(
        'Host',
        order_by=Host.id,
        back_populates='mission',
        cascade='save-update, merge, delete, delete-orphan'
    )

    # --------------------------------------------------------------------

    @hybrid_method
    def get_nb_services(self) -> int:
        """Return the total number of services inside the mission scope"""
        nb = 0
        for host in self.hosts:
            nb += len(host.services)
        return nb

    # --------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            '<Mission(name="{name}", comment="{comment}", '
            'creation_date="{creation_date}")>'.format(
                name=self.name,
                comment=self.comment,
                creation_date=self.creation_date
            )
        )
