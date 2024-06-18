import os, re
import numpy as np
from tqdm import tqdm
from pwdata.calculators.const import elements, ELEMENTTABLE
from pwdata.image import Image
from ase.io import read

class EXTXYZ(object):
    def __init__(self, xyz_file, index) -> None:
        self.image_list:list[Image] = []
        self.number_pattern = re.compile(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
        self.load_xyz_file(xyz_file, index)

    def get(self):
        return self.image_list

    def load_xyz_file(self, xyz_file, index):
        Atoms = read(xyz_file, index=index, format='extxyz')
        if isinstance(Atoms, list):
            for i in tqdm(range(len(Atoms)), desc="Converting images"):
                image = Image()
                image.formula = Atoms[i].symbols.formula._formula
                image.pbc = Atoms[i].pbc
                image.atom_nums = Atoms[i].get_global_number_of_atoms()
                image.atom_type = [ELEMENTTABLE[type] for type in Atoms[i].symbols.formula._count.keys()]
                image.atom_type_num = [num for num in Atoms[i].symbols.formula._count.values()]
                image.atom_types_image = Atoms[i].numbers
                # image.atom_types_image = Atoms[i].get_chemical_symbols()
                image.lattice = Atoms[i].cell.array
                image.position = Atoms[i].positions
                image.cartesian = True
                image.force = Atoms[i].get_forces()
                image.Ep = Atoms[i].info['energy']
                # If Atomic-Energy is not in the file, calculate it from the Ep
                atomic_energy, _, _, _ = np.linalg.lstsq([image.atom_type_num], np.array([image.Ep]), rcond=1e-3)
                atomic_energy = np.repeat(atomic_energy, image.atom_type_num)
                image.atomic_energy = atomic_energy.tolist()
                try:
                    stress = Atoms[i].get_stress(voigt=False)
                except AttributeError:
                    pass
                else:
                    # virial = -stress * volume
                    image.stress = - Atoms[i].get_volume() * stress
                image.format = 'extxyz'
                self.image_list.append(image)
        else:
            image = Image()
            image.formula = Atoms.get_chemical_formula()
            image.pbc = Atoms.pbc
            image.atom_nums = Atoms.get_global_number_of_atoms()
            image.atom_type = [ELEMENTTABLE[type] for type in Atoms.symbols.formula._count.keys()]
            image.atom_type_num = [num for num in Atoms.symbols.formula._count.values()]
            image.atom_types_image = Atoms.numbers
            # image.atom_types_image = Atoms.get_chemical_symbols()
            image.lattice = Atoms.cell.array
            image.position = Atoms.positions
            image.cartesian = True
            image.force = Atoms.get_forces()
            image.Ep = Atoms.info['energy']
            # If Atomic-Energy is not in the file, calculate it from the Ep
            atomic_energy, _, _, _ = np.linalg.lstsq([image.atom_type_num], np.array([image.Ep]), rcond=1e-3)
            atomic_energy = np.repeat(atomic_energy, image.atom_type_num)
            image.atomic_energy = atomic_energy.tolist()
            try:
                stress = Atoms.get_stress(voigt=False)
            except AttributeError:
                pass
            else:
                image.stress = - Atoms.get_volume() * stress
            image.format = 'extxyz'
            self.image_list.append(image)


def save_to_extxyz(image_data_all: list, output_path: str, data_name: str, write_patthen='w'):
    data_name = open(os.path.join(output_path, data_name), write_patthen)
    for i in range(len(image_data_all)):
        image_data = image_data_all[i]
        if not image_data.cartesian:
            image_data._set_cartesian()
        data_name.write("%d\n" % image_data.atom_nums)
        # data_name.write("Iteration: %s\n" % image_data.iteration)
        output_head = 'Lattice="%.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f" Properties=species:S:1:pos:R:3:forces:R:3:local_energy:R:1 pbc="T T T" energy={} '.format(image_data.Ep)
        output_extended = (image_data.lattice[0][0], image_data.lattice[0][1], image_data.lattice[0][2], 
                            image_data.lattice[1][0], image_data.lattice[1][1], image_data.lattice[1][2], 
                            image_data.lattice[2][0], image_data.lattice[2][1], image_data.lattice[2][2])
        if image_data.stress is not None:
            output_head += 'stress="%.8f %.8f %.8f %.8f %.8f %.8f %.8f %.8f %.8f"'
            output_extended += (image_data.stress[0][0], image_data.stress[0][1], image_data.stress[0][2], 
                                image_data.stress[1][0], image_data.stress[1][1], image_data.stress[1][2], 
                                image_data.stress[2][0], image_data.stress[2][1], image_data.stress[2][2])
        output_head += '\n'
        data_name.write(output_head % output_extended)
        for j in range(image_data.atom_nums):
            properties_format = "%s %14.8f %14.8f %14.8f %14.8f %14.8f %14.8f %14.8f\n"
            properties = (elements[image_data.atom_types_image[j]], image_data.position[j][0], image_data.position[j][1], image_data.position[j][2], 
                            image_data.force[j][0], image_data.force[j][1], image_data.force[j][2], 
                            image_data.atomic_energy[j])
            data_name.write(properties_format % properties)
    data_name.close()
    print("Convert to %s successfully!" % data_name)
