from web3 import Web3
from hexbytes.main import HexBytes
# from web3._utils.datatypes import Contract

class DarkPid:

    def __init__(self,pid_hash,ark_id,externa_pid_list,externa_url_list,payload:dict,owner) -> None:
        
        if type(pid_hash) == HexBytes:
            self.pid_hash = pid_hash
        else:
            self.pid_hash = HexBytes(pid_hash)

        self.ark = ark_id
        self.external_pid_list = externa_pid_list
        self.external_url = externa_url_list
        self.payload = payload
        self.responsible = owner

    def to_dict(self):
        """
        Converts the attributes of the class object into a dictionary.

        Returns:
            dict: A dictionary representation of the class object's attributes.
        """
        return vars(self)
    
    def __is_bc_valid(bc_output):
        """
        Validates the structure and types of the provided output.

        Parameters:
            output (tuple): The output to be validated.

        Returns:
            bool: True if the output is valid, False otherwise.
        """
        if len(bc_output) != 6:
            return False

        if not isinstance(bc_output[0], bytes) or not isinstance(bc_output[1], str):
            return False

        if not isinstance(bc_output[2], list) or not isinstance(bc_output[3], bytes):
            return False

        if not isinstance(bc_output[4], bytes):
            return False

        return True

    def populate(dark_object,epid_db_contract,url_db_contract,payload_obj):
        assert DarkPid.__is_bc_valid(dark_object) == True, "Invalid Blockchain Output"
        # TODO: VALIDADE epid_db_contract
        # assert type(epid_db_contract) == Contract, "epid_db_contract must be web3._utils.datatypes.Contract type"

        # populate external pids
        external_pids = []
        for ext_pid in dark_object[2]:
            ext_pid = Web3.to_hex(ext_pid)
            # epid = epid_db.functions.get(ext_pid).call()
            get_func = epid_db_contract.get_function_by_signature('get(bytes32)')
            epid = get_func(ext_pid).call()

            pid_object = {'hash_id': ext_pid, 
                            'value' : epid[2], 
                            'owner:' : epid[-1]
                        }
            external_pids.append(pid_object)
        
        # deprecated

        zbytes32 = dark_object[3].hex().rstrip("0")
        if len(zbytes32) % 2 != 0:
            zbytes32 = zbytes32 + '0'
        try:    
            zbytes32 = bytes.fromhex(zbytes32).decode('utf8')
            externa_url_list = ''
        except UnicodeDecodeError:
            get_url = url_db_contract.get_function_by_signature('get(bytes32)')
            url_obj = get_url(Web3.to_hex(dark_object[3])).call()
            externa_url_list = url_obj[2]

        # if len(zbytes32) != 0:
        #     externa_url_list = zbytes32
        # else:
        #     externa_url_list = ''
        # for ext_link in dark_object[3]:
        #     externa_url_list.append(ext_link)

        pid_hash_id = Web3.to_hex(dark_object[0])
        pid_ark_id = dark_object[1]
        
        # payload = dark_object[-2].hex().rstrip("0")
        # payload_hash = dark_object[-2]

        payload = {}
        if payload_obj != None:
            payload = payload_obj.attributes
        #TODO: CRIAR O SCHEMA

        owner = dark_object[-1]
        

        return DarkPid(pid_hash_id,pid_ark_id,external_pids,externa_url_list,payload,owner)
    
    def populateDark(dark_object,epid_db_contract,url_db_contract):
        assert DarkPid.__is_bc_valid(dark_object) == True, "Invalid Blockchain Output"
        # TODO: VALIDADE epid_db_contract
        # assert type(epid_db_contract) == Contract, "epid_db_contract must be web3._utils.datatypes.Contract type"

        # populate external pids
        external_pids = []
        for ext_pid in dark_object[2]:
            ext_pid = Web3.to_hex(ext_pid)
            # epid = epid_db.functions.get(ext_pid).call()
            get_func = epid_db_contract.get_function_by_signature('get(bytes32)')
            epid = get_func(ext_pid).call()

            pid_object = {'hash_id': ext_pid, 
                            'value' : epid[2], 
                            'owner:' : epid[-1]
                        }
            external_pids.append(pid_object)
        
        # deprecated

        zbytes32 = dark_object[3].hex().rstrip("0")
        if len(zbytes32) % 2 != 0:
            zbytes32 = zbytes32 + '0'
        try:    
            zbytes32 = bytes.fromhex(zbytes32).decode('utf8')
            externa_url_list = ''
        except UnicodeDecodeError:
            get_url = url_db_contract.get_function_by_signature('get(bytes32)')
            url_obj = get_url(Web3.to_hex(dark_object[3])).call()
            externa_url_list = url_obj[2]

        # if len(zbytes32) != 0:
        #     externa_url_list = zbytes32
        # else:
        #     externa_url_list = ''
        # for ext_link in dark_object[3]:
        #     externa_url_list.append(ext_link)

        pid_hash_id = Web3.to_hex(dark_object[0])
        pid_ark_id = dark_object[1]
        
        # payload = dark_object[-2].hex().rstrip("0")
        payload_hash = dark_object[-2]
        # b'\x00' * 32 = 0
        if payload_hash != b'\x00' * 32:
            payload=''
            print('0')
            print(payload_hash)
        else:
            dp = DarkPid(pid_hash_id,pid_ark_id,external_pids,externa_url_list,'','')
            # self
            # get_payload_schema = url_db_contract.get_function_by_signature('get_payload_schema(bytes32)')
            # get_payload = url_db_contract.get_function_by_signature('get_payload(bytes32)')
            # payload_obj = get_payload(Web3.to_hex(payload_hash)).call()

            # payload_schema = get_payload_schema(Web3.to_hex(payload_obj[0])).call()

            # print(payload_schema)

            payload = 'TODO AJUSTAR'

        owner = dark_object[-1]
        

        return DarkPid(pid_hash_id,pid_ark_id,external_pids,externa_url_list,payload,owner)

        
class ExeternalPid:
    def __init__(self,id_hash,schema,value,creator) -> None:
        self.id = id_hash
        self.schema = schema
        self.pid_str_value = value
        self.creator_addr = creator

    def to_dict(self):
        """
        Converts the attributes of the class object into a dictionary.

        Returns:
            dict: A dictionary representation of the class object's attributes.
        """
        return vars(self)
    
class PayloadSchema:
    def __init__(self,schema_hash,schema_name:str,configured:bool) -> None:
        self.id = schema_hash
        self.schema_name = schema_name
        self.attribute_list = []
        self.configured = configured

    def to_dict(self):
        """
        Converts the attributes of the class object into a dictionary.

        Returns:
            dict: A dictionary representation of the class object's attributes.
        """
        return vars(self)
    
    @staticmethod
    def populate(dark_object):
        # assert DarkPid.__is_bc_valid(dark_object) == True, "Invalid Blockchain Output"

        schema_name = dark_object[0].lower()
        att_list = dark_object[1]
        confa = dark_object[2]
        
        ps = PayloadSchema('',schema_name,confa)
        
        if len(att_list) > 0:
            for att in att_list:
                ps.attribute_list.append(att.lower())

        return ps

class Payload:
    def __init__(self) -> None:
        self.payload_schema = None
        self.attributes = None

    def to_dict(self):
        """
        Converts the attributes of the class object into a dictionary.

        Returns:
            dict: A dictionary representation of the class object's attributes.
        """
        return vars(self)
    
    @staticmethod
    def populate(dark_object, payload_schema:PayloadSchema):
        # assert DarkPid.__is_bc_valid(dark_object) == True, "Invalid Blockchain Output"
        att_value_list = dark_object[1]
        
        payload = Payload()
        payload.payload_schema = payload_schema

        payload.attributes = {}
        for i in range(len(att_value_list)):
            payload.attributes[payload_schema.attribute_list[i]] = att_value_list[i]

        return payload