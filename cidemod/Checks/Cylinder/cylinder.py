from cideMOD.mesh.base_mesher import SubdomainGenerator, BaseMesher, SubdomainMapper
from dolfin import (
    Mesh, 
    MeshTransformation,
    Point, 
    XDMFFile,
    MeshFunction, 
    CompiledSubDomain,
    Measure,
    BoxMesh,
)
from multiphenics import MeshRestriction

class Cylinder(BaseMesher):
    def build_mesh(self):
        n = self.num_components

        print('Building simple cylindrical mesh from cylinder_3.xml')

        #DEBUG: box
        Nx=6
        Ny=6
        Nz=6

        p1 = Point(0,0,0)
        p2 = Point(n,1,1)
        self.mesh = BoxMesh(p1,p2, Nx*n, Ny or Nx, Nz or Nx)
        #Load cylinder length 3 in z-direction, radius 0.5
        #self.mesh=Mesh("cylinder_3.xml")
        #Define class to rotate and translate
        #rot=MeshTransformation 
        #rotation
        #rot.rotate(self.mesh,90,1)
        #Translation
        #tx=Point(1.5,0,0)
        #tz=Point(0,0,-1.5)
        #rot.translate(self.mesh, tx)
        #rot.translate(self.mesh,tz)
        #Cylinder now along x-axis rather than z-axis in order to be comptatible with cide

        #Cylinder dimension
        self.dimension = self.mesh.geometric_dimension()

        subdomain_generator = SubdomainGenerator()
        #Defines the tags for each part of the battery (no CC in this case)
        self.field_data['anode'] = 1
        self.field_data['separator'] = 2
        self.field_data['cathode'] = 3
        self.field_data['negativeCC'] = 4
        self.field_data['positiveCC'] = 5
        self.field_data['negativePlug'] = 6
        self.field_data['positivePlug'] = 7
        self.field_data['interfaces'] = {
            'anode-separator': 1,
            'cathode-separator': 2,
            'anode-CC': 3,
            'cathode-CC': 4,
        }

        # Mark boundaries
        boundaries = MeshFunction("size_t", self.mesh, self.mesh.topology().dim() - 1, 0)

        if self.structure[-1] in ('c','pcc') or not 'c' in self.structure:
            negativetab = subdomain_generator.set_boundary(0)
            positivetab = subdomain_generator.set_boundary(n)
        else:
            negativetab = subdomain_generator.set_boundary(n)
            positivetab = subdomain_generator.set_boundary(0)
        negativetab.mark(boundaries, self.field_data['negativePlug'])
        positivetab.mark(boundaries, self.field_data['positivePlug'])

        tabs = subdomain_generator.set_boundaries(0, n)

        self.boundaries = boundaries

        #Mark subdomains
        subdomains = MeshFunction("size_t", self.mesh, self.mesh.topology().dim(), 99)

        #Looking for corresponding indices in structure, we put this here to be consistent with cide
        anode_list = [index for index, element in enumerate(self.structure) if element == 'a']
        cathode_list = [index for index, element in enumerate(self.structure) if element == 'c']
        separator_list = [index for index, element in enumerate(self.structure) if element == 's']
        positive_cc_list = [index for index, element in enumerate(self.structure) if element == 'pcc']
        negative_cc_list = [index for index, element in enumerate(self.structure) if element == 'ncc']

        tol=1e-3
        #Define the subdomains for the anode, separator, cathode with a much higher tolerance than the one used by cide
        anode=CompiledSubDomain("x[0]>=-tol && x[0]<=1+tol",tol=tol)
        separator=CompiledSubDomain("x[0]>=1-tol && x[0]<=2+tol",tol=tol)
        cathode=CompiledSubDomain("x[0]>=2-tol && x[0]<=3+tol",tol=tol)
        #to be complete
        negative_cc = subdomain_generator.set_domain(negative_cc_list)
        positive_cc = subdomain_generator.set_domain(positive_cc_list)

        #electrodes = subdomain_generator.electrodes(self.structure)
        electrodes=CompiledSubDomain("(x[0]>=-tol && x[0]<=1+tol) || (x[0]>=2-tol && x[0]<=3+tol)",tol=tol)
        #electrolyte = subdomain_generator.electrolyte(self.structure)
        electrolyte=CompiledSubDomain("x[0]>=-tol && x[0]<=3+tol",tol=tol)
        #solid_conductor = subdomain_generator.solid_conductor(self.structure)
        solid_conductor=electrodes
        #Aka, never, no current collectprs
        current_colectors = CompiledSubDomain("x[0]>0 && x[0]<0",tol=tol)

        #CCs will not be marked, but anode, separator, cathode should be correct
        negative_cc.mark(subdomains, self.field_data['negativeCC'])
        anode.mark(subdomains,self.field_data['anode'])
        separator.mark(subdomains,self.field_data['separator'])
        cathode.mark(subdomains,self.field_data['cathode'])
        positive_cc.mark(subdomains, self.field_data['positiveCC'])

        self.subdomains = subdomains
        self.check_subdomains(self.subdomains, self.field_data)

        #xdmf file to verify subdomains 
        XDMFFile("Cylinder_checks/cylinder_verify_subdomains.xdmf").write(self.subdomains)

        #We now define the interfaces between the different parts of the battery
        #Aka now we have objects of dimension 2
        interfaces = MeshFunction("size_t", self.mesh, self.mesh.topology().dim() -1, 0)

        #Identify the different interfaces, we put this here for completeness,
        #not used in out version
        negativeCC_interfaces = set(negative_cc_list).union([i+1 for i in negative_cc_list])
        anode_interfaces = set(anode_list).union([i+1 for i in anode_list])
        separator_interfaces = set(separator_list).union([i+1 for i in separator_list])
        cathode_interfaces = set(cathode_list).union([i+1 for i in cathode_list])
        positiveCC_interfaces = set(positive_cc_list).union([i+1 for i in positive_cc_list])
        anode_separator_interface_list = anode_interfaces.intersection(separator_interfaces)
        anode_CC_interface_list = anode_interfaces.intersection(negativeCC_interfaces)
        cathode_separator_interface_list = cathode_interfaces.intersection(separator_interfaces)
        cathode_CC_interface_list = cathode_interfaces.intersection(positiveCC_interfaces)
                
        #Define interfaces, no CC means interface on that edge is purely superificial
        #Condition should be equivalent to near
        anode_separator_interface=CompiledSubDomain("(x[0]-1<tol && x[0]-1>0)|| (1-x[0]<tol && 1-x[0]>0)",tol=tol)
        cathode_separator_interface=CompiledSubDomain("(x[0]-2<tol && x[0]-2>0)|| (2-x[0]<tol && 2-x[0]>0)",tol=tol)
        anode_CC_interface = CompiledSubDomain("(x[0]-0<tol && x[0]-0>0)|| (0-x[0]<tol && 0-x[0]>0)",tol=tol)
        cathode_CC_interface = CompiledSubDomain("(x[0]-3<tol && x[0]-3>0)|| (3-x[0]<tol && 3-x[0]>0)",tol=tol)
        
        anode_separator_interface.mark(interfaces,self.field_data['interfaces']['anode-separator'])
        cathode_separator_interface.mark(interfaces,self.field_data['interfaces']['cathode-separator'])
        anode_CC_interface.mark(interfaces,self.field_data['interfaces']['anode-CC'])
        cathode_CC_interface.mark(interfaces,self.field_data['interfaces']['cathode-CC'])

        self.interfaces = interfaces

        #xdmf file to verify subdomains 
        XDMFFile("Cylinder_checks/cylinder_verify_interfaces.xdmf").write(self.interfaces)

        # Define restriction in equivalent manner to cide 
        self.anode = MeshRestriction(self.mesh, anode)
        self.separator = MeshRestriction(self.mesh, separator)
        self.cathode = MeshRestriction(self.mesh, cathode)
        self.positiveCC = MeshRestriction(self.mesh, positive_cc)
        self.negativeCC = MeshRestriction(self.mesh, negative_cc)
        self.field_restrictions = {
            'anode':self.anode, 'separator':self.separator, 'cathode':self.cathode, 'positiveCC':self.positiveCC, 'negativeCC':self.negativeCC
        }
        self.electrodes = MeshRestriction(self.mesh, electrodes)
        self.electrolyte = MeshRestriction(self.mesh, electrolyte)
        self.solid_conductor = MeshRestriction(self.mesh, solid_conductor)
        self.current_colectors = MeshRestriction(self.mesh, current_colectors)
        self.electrode_cc_interfaces = MeshRestriction(self.mesh, [anode_CC_interface, cathode_CC_interface])
        self.positive_tab = MeshRestriction(self.mesh, positivetab)
        self.tabs = MeshRestriction(self.mesh, tabs)

        # Define measure in equivalent manner to cide
        a_s_c_order = all([self.structure[i+1]=='s' for i, el in enumerate(self.structure) if el is 'a'])
        def int_dir(default_dir="+"):
            assert default_dir in ("+","-")
            reversed_dir = "-" if default_dir == "+" else "-"
            return default_dir if a_s_c_order else reversed_dir
        meta = {"quadrature_degree":2}
        self.dx = Measure('dx', domain=self.mesh, subdomain_data=subdomains, metadata=meta)
        self.dx_a = self.dx(self.field_data['anode'])
        self.dx_s = self.dx(self.field_data['separator'])
        self.dx_c = self.dx(self.field_data['cathode'])
        self.dx_pcc = self.dx(self.field_data['positiveCC'])
        self.dx_ncc = self.dx(self.field_data['negativeCC'])
        self.ds = Measure('ds', domain=self.mesh, subdomain_data=boundaries, metadata=meta)
        self.ds_a = self.ds(self.field_data['negativePlug'])
        self.ds_c = self.ds(self.field_data['positivePlug'])
        self.dS = Measure('dS', domain=self.mesh, subdomain_data=interfaces, metadata=meta)
        self.dS_as = self.dS(self.field_data['interfaces']['anode-separator'], metadata={**meta, "direction": int_dir("+")})
        self.dS_sa = self.dS(self.field_data['interfaces']['anode-separator'], metadata={**meta, "direction": int_dir("-")})
        self.dS_sc = self.dS(self.field_data['interfaces']['cathode-separator'], metadata={**meta, "direction": int_dir("+")})
        self.dS_cs = self.dS(self.field_data['interfaces']['cathode-separator'], metadata={**meta, "direction": int_dir("-")})
        self.dS_cc_a = self.dS(self.field_data['interfaces']['anode-CC'], metadata={**meta, "direction": int_dir("+")})
        self.dS_a_cc = self.dS(self.field_data['interfaces']['anode-CC'], metadata={**meta, "direction": int_dir("-")})
        self.dS_cc_c = self.dS(self.field_data['interfaces']['cathode-CC'], metadata={**meta, "direction": int_dir("-")})
        self.dS_c_cc = self.dS(self.field_data['interfaces']['cathode-CC'], metadata={**meta, "direction": int_dir("+")})

        print('Finished building cylinder mesh')