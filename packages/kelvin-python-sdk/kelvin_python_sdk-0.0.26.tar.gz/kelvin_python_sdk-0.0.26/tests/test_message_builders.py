""" Test Message Builders """

import uuid
from datetime import datetime, timedelta

from kelvin.krn import KRNAsset, KRNAssetDataStream
from kelvin.message import ControlChange, ControlChangeMsg, Recommendation, RecommendationMsg


def test_builder_control_change() -> None:
    now = datetime.now()

    cc = ControlChange(resource=KRNAssetDataStream("asset1", "metric1"), expiration_date=now, payload=25)

    cc_msg = cc.to_message()

    assert isinstance(cc_msg, ControlChangeMsg)
    assert cc_msg.payload.expiration_date == cc.expiration_date
    assert cc_msg.payload.payload == cc.payload
    assert cc_msg.resource == cc.resource


def test_builder_recommendation() -> None:
    now = datetime.now()
    cc_uuid = uuid.uuid4()

    cc = ControlChange(
        resource=KRNAssetDataStream("asset1", "metric1"), expiration_date=now, payload=25, control_change_id=cc_uuid
    )

    rec = Recommendation(
        resource=KRNAsset("asset1"),
        type="e2e_recommendation",
        control_changes=[cc],
        expiration_date=timedelta(minutes=5),
        auto_accepted=True,
    )

    rec_msg = rec.to_message()
    assert isinstance(rec_msg, RecommendationMsg)
