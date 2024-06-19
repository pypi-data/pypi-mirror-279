import pytest
from JOPLEn.enums import CellModel, LossType
from JOPLEn.partitioner import (
    CBPartition,
    ExtraTreePartition,
    GBPartition,
    LGBMPartition,
    LinearForestPartition,
    RFPartition,
    VPartition,
)
from JOPLEn.singletask import JOPLEn
from JOPLEn.st_loss import LogisticLoss, SquaredError
from JOPLEn.st_penalty import (
    Group21Norm,
    GroupInf1Norm,
    L1Norm,
    NuclearNorm,
    SquaredFNorm,
)


def gen_train_data(is_classification):
    from sklearn.datasets import make_classification, make_regression
    from sklearn.model_selection import train_test_split

    kwargs = {
        "n_samples": 1000,
        "n_features": 20,
        "n_informative": 10,
        "random_state": 0,
    }

    if is_classification:
        x, y = make_classification(**kwargs, n_classes=2)
        y = y.flatten()
    else:
        x, y = make_regression(**kwargs, n_targets=1, noise=0.1)

    # Split the dataset into training and test sets
    x_train, x_val, y_train, y_val = train_test_split(
        x, y, test_size=0.2, random_state=0
    )

    return x_train, y_train, x_val, y_val


# Just makes sure that the model runs without any errors
@pytest.mark.parametrize(
    "part",
    [
        VPartition,
        ExtraTreePartition,
        LGBMPartition,
        CBPartition,
        RFPartition,
        GBPartition,
        LinearForestPartition,
    ],
)
@pytest.mark.parametrize("loss_fn", [SquaredError, LogisticLoss])
@pytest.mark.parametrize("cell_model", [CellModel.linear, CellModel.constant])
@pytest.mark.parametrize(
    "reg",
    [
        SquaredFNorm,
        Group21Norm,
        GroupInf1Norm,
        NuclearNorm,
        L1Norm,
    ],
)
def test_st_reg(part, loss_fn, cell_model, reg):
    x_train, y_train, x_val, y_val = gen_train_data(
        is_classification=(loss_fn().loss_type == LossType.binary_classification)
    )

    jp = JOPLEn(
        partitioner=part,
        n_cells=8,
        n_partitions=5,
        loss_fn=loss_fn,
        cell_model=cell_model,
        mu=1e-3,
        max_iters=100,
        early_stop=False,
        rescale=False,
        regularizers=[reg(lam=0.01)],
    )

    jp.fit(
        x_train,
        y_train,
        val_x=x_val,
        val_y=y_val,
        print_epochs=10,
    )
