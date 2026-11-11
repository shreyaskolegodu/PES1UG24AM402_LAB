import pytest
from car_insurance_premium import annual_premium, no_claim_bonus, claim_payout

@pytest.mark.parametrize("args,expected", [
    (("sedan",30,0,False),9600),
    (("hatchback",18,1,True),11500),
    (("suv",60,3,False),34000),
    (("sedan",24,2,False),16000),
    (("sedan",25,1,False),12000),
    (("sedan",59,0,True),9100),
])
def test_premium(args, expected):
    assert annual_premium(*args) == expected

@pytest.mark.parametrize("args,message", [
    (("truck",30,0,False),"unknown car type"),
    (("sedan",17,0,False),"driver too young"),
])
def test_invalid_premium(args,message):
    with pytest.raises(ValueError, match=message):
        annual_premium(*args)

@pytest.mark.parametrize("years,expected", [(0,0),(1,20),(2,20),(3,35),(4,35),(5,50),(6,50)])
def test_bonus(years,expected):
    assert no_claim_bonus(years) == expected

def test_invalid_bonus():
    with pytest.raises(ValueError, match="invalid years"):
        no_claim_bonus(-1)

@pytest.mark.parametrize("args,expected", [
    ((500,10000,100,True),10000),
    ((100,10000,100,False),0),
    ((0,10000,100,False),0),
    ((1100,10000,100,False),1000),
    ((10100,10000,100,False),10000),
    ((10101,10000,100,False),10000),
])
def test_payout(args,expected):
    assert claim_payout(*args) == expected

@pytest.mark.parametrize("args", [(-1,10000,0,False),(100,10000,-1,False)])
def test_invalid_payout(args):
    with pytest.raises(ValueError, match="invalid amount"):
        claim_payout(*args)
