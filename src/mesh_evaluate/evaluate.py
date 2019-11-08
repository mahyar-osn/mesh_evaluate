"""
A simple script to evaluate user-define element xi locations.
"""

import os
import argparse
import re

from opencmiss.zinc.context import Context
from opencmiss.zinc.status import OK as ZINC_OK


class ProgramArguments(object):
    pass


def evaluate(input_mesh, dim, xi_loc):
    context = Context("Scaffold")
    region = context.getDefaultRegion()
    region.readFile(input_mesh)
    field_module = region.getFieldmodule()
    field = field_module.findFieldByName("coordinates")
    cache = field_module.createFieldcache()
    xi = xi_loc
    mesh = field_module.findMeshByDimension(dim)
    if len(xi) != dim:
        raise TypeError("Number of xi coordinates is not valid for {} dimension".format(dim))
    el_iter = mesh.createElementiterator()
    element = el_iter.next()
    while element.isValid():
        cache.setMeshLocation(element, xi)
        result, out_values = field.evaluateReal(cache, 3)

        if result == ZINC_OK:
            print(element.getIdentifier(), out_values)
        else:
            break
        element = el_iter.next()


def main():
    args = parse_args()
    if os.path.exists(args.input_mesh):
        if args.dimension is None:
            dimension = 3
        else:
            dimension = int(args.dimension)

        if args.xi_locations is None:
            xi_locations = [0.5, 0.5, 0.5]
        else:
            xi_locations = float(args.xi_locations)
            if not isinstance(xi_locations, list):
                xi_locations = [xi_locations] * dimension

        evaluate(args.input_mesh, dimension, xi_locations)


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate element xi locations form an input .exf format mesh.")
    parser.add_argument("input_mesh", help="Location of the input exf file.")
    parser.add_argument("-d", "--dimension", help="Dimension of the mesh i.e. 1, 2, or3. "
                                                "[defaults 3D i.e. Tri-cubic.]")
    parser.add_argument("-xi", "--xi_locations", help="The xi coordinates to evaluate. "
                                                "[defaults to 0.5.]")

    program_arguments = ProgramArguments()
    parser.parse_args(namespace=program_arguments)

    return program_arguments


if __name__ == '__main__':
    main()
