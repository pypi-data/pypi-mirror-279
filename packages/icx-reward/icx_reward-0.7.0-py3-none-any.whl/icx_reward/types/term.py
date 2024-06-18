from typing import List

from icx_reward.rpc import RPC
from icx_reward.types.prep import PRep
from icx_reward.types.rate import Rate
from icx_reward.types.reward_fund import RewardFund


class Term:
    def __init__(self,
                 block_height: int,
                 bond_requirement: Rate,
                 end_block_height: int,
                 iiss_version: int,
                 is_decentralized: bool,
                 main_prep_count: int,
                 minimum_bond: int,
                 period: int,
                 revision: int,
                 reward_fund: RewardFund,
                 sequence: int,
                 start_block_height: int,
                 total_delegated: int,
                 total_power: int,
                 total_supply: int,
                 ):
        self.block_height = block_height
        self.bond_requirement = bond_requirement
        self.end_block_height = end_block_height
        self.iiss_version = iiss_version
        self.is_decentralized = is_decentralized
        self.main_prep_count = main_prep_count
        self.minimum_bond = minimum_bond
        self.period = period
        self.revision = revision
        self.reward_fund = reward_fund
        self.sequence = sequence
        self.start_block_height = start_block_height
        self.total_delegated = total_delegated
        self.total_power = total_power
        self.total_supply = total_supply

    def __repr__(self):
        return (f"Term('block_height': '{self.block_height}', 'bond_requirement': {self.bond_requirement}, "
                f"'end_block_height': {self.end_block_height}, 'iiss_version': {self.iiss_version}), "
                f"'is_decentralized': {self.is_decentralized}, 'main_prep_count': {self.main_prep_count}), "
                f"'minimum_bond': {self.minimum_bond}, 'preiod': {self.period}), "
                f"'revision': {self.revision}, 'reward_fund': {self.reward_fund}), 'sequence': {self.sequence}, "
                f"'start_block_height': {self.start_block_height}, 'total_delegated': {self.total_delegated}), "
                f"'total_power': {self.total_power}, 'total_supply': {self.total_supply})"
                f")"
                )

    def info(self) -> str:
        return f"Term('sequence': {self.sequence}', start_height: {self.start_block_height}, 'end_block_height': {self.end_block_height})"

    def is_prep(self, address: str):
        return address in self.preps

    @staticmethod
    def from_dict(values: dict):
        if "bondRequirement" in values:
            br = Rate(int(values["bondRequirement"], 16), Rate.DENOM_OLD)
        else:
            br = Rate(int(values["bondRequirementRate"], 16))
        return Term(
            block_height=int(values["blockHeight"], 16),
            bond_requirement= br,
            end_block_height=int(values["endBlockHeight"], 16),
            iiss_version=int(values["iissVersion"], 16),
            is_decentralized=bool(int(values["isDecentralized"], 16)),
            main_prep_count=int(values["mainPRepCount"], 16),
            minimum_bond=int(values.get("minimumBond", "0x0"), 16),
            period=int(values["period"], 16),
            revision=int(values["revision"], 16),
            reward_fund=RewardFund.from_dict(values["rewardFund"]),
            sequence=int(values["sequence"], 16),
            start_block_height=int(values["startBlockHeight"], 16),
            total_delegated=int(values["totalDelegated"], 16),
            total_power=int(values["totalPower"], 16),
            total_supply=int(values["totalSupply"], 16),
        )
