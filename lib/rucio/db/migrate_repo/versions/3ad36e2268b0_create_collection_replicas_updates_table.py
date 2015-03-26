# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Martin Barisits, <martin.barisits@cern.ch>, 2015

"""Create collection_replicas_updates table

Revision ID: 3ad36e2268b0
Revises: ae2a56fcc89
Create Date: 2015-03-16 15:32:59.620185

"""

# revision identifiers, used by Alembic.
revision = '3ad36e2268b0'
down_revision = '42db2617c364'

from alembic import op, context
import sqlalchemy as sa

from rucio.db.constants import DIDType
from rucio.db.types import GUID


def upgrade():
    if context.get_context().dialect.name != 'sqlite':
        op.add_column('collection_replicas', sa.Column('available_replicas_cnt', sa.BigInteger()))
        op.add_column('collection_replicas', sa.Column('available_bytes', sa.BigInteger()))

    op.create_table('updated_col_rep',
                    sa.Column('id', GUID()),
                    sa.Column('scope', sa.String(25)),
                    sa.Column('name', sa.String(255)),
                    sa.Column('did_type', DIDType.db_type(name='UPDATED_COL_REP_TYPE_CHK')),
                    sa.Column('rse_id', GUID()),
                    sa.Column('updated_at', sa.DateTime),
                    sa.Column('created_at', sa.DateTime))

    if context.get_context().dialect.name != 'sqlite':
        op.create_primary_key('UPDATED_COL_REP_PK', 'updated_col_rep', ['id'])
        op.create_check_constraint('UPDATED_COL_REP_SCOPE_NN', 'updated_col_rep', 'scope IS NOT NULL')
        op.create_check_constraint('UPDATED_COL_REP_NAME_NN', 'updated_col_rep', 'name IS NOT NULL')
        op.create_index('UPDATED_COL_REP_SNR_IDX', 'updated_col_rep', ['scope', 'name', 'rse_id'])


def downgrade():
    op.drop_column('collection_replicas', 'available_replicas_cnt')
    op.drop_column('collection_replicas', 'available_bytes')

    if context.get_context().dialect.name == 'postgresql':
        op.drop_constraint('UPDATED_COL_REP_PK', 'updated_col_rep', type_='primary')
        op.drop_constraint('UPDATED_COL_REP_SCOPE_NN', 'updated_col_rep')
        op.drop_constraint('UPDATED_COL_REP_NAME_NN', 'updated_col_rep')
        op.drop_constraint('UPDATED_COL_REP_TYPE_CHK', 'updated_col_rep')
        op.drop_index('UPDATED_COL_REP_SNR_IDX', 'updated_col_rep')
    op.drop_table('updated_col_rep')