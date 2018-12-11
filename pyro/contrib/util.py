from __future__ import absolute_import, division, print_function

from collections import OrderedDict
import torch


def get_indices(labels, sizes=None, tensors=None):
    indices = []
    start = 0
    if sizes is None:
        sizes = OrderedDict([(l, t.shape[0]) for l, t in tensors.items()])
    for label in sizes:
        end = start+sizes[label]
        if label in labels:
            indices.extend(range(start, end))
        start = end
    return torch.tensor(indices)


def tensor_to_dict(sizes, tensor, subset=None):
    if subset is None:
        subset = sizes.keys()
    start = 0
    out = {}
    for label, size in sizes.items():
        end = start + size
        if label in subset:
            out[label] = tensor[..., start:end]
        start = end
    return out


def rmm(A, B):
    """Shorthand for `matmul`."""
    return torch.matmul(A, B)


def rmv(A, b):
    """Tensorized matrix vector multiplication of rightmost dimensions."""
    return torch.matmul(A, b.unsqueeze(-1)).squeeze(-1)


def rvv(a, b):
    """Tensorized vector vector multiplication of rightmost dimensions."""
    return torch.matmul(a.unsqueeze(-2), b.unsqueeze(-1)).squeeze(-2).squeeze(-1)


def lexpand(A, *dimensions):
    """Expand tensor, adding new dimensions on left."""
    return A.expand(tuple(dimensions) + A.shape)


def rexpand(A, *dimensions):
    """Expand tensor, adding new dimensions on right."""
    return A.view(A.shape + (1,)*len(dimensions)).expand(A.shape + tuple(dimensions))


def rdiag(v):
    """Converts the rightmost dimension to a diagonal matrix."""
    return rexpand(v, v.shape[-1])*torch.eye(v.shape[-1])


def rtril(M, diagonal=0):
    """Takes the lower-triangular of the rightmost 2 dimensions."""
    return M*torch.tril(torch.ones(M.shape[-2], M.shape[-1]), diagonal=diagonal)


def hessian(y, xs):
    dys = torch.autograd.grad(y, xs, create_graph=True)
    flat_dy = torch.cat([dy.reshape(-1) for dy in dys])
    H = []
    for dyi in flat_dy:
        Hi = torch.cat([Hij.reshape(-1) for Hij in torch.autograd.grad(dyi, xs, retain_graph=True)])
        H.append(Hi)
    H = torch.stack(H)
    return H
