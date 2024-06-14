# coding: utf-8

"""
    iparapheur

    iparapheur v5.x main core application.  The main link between every sub-services, integrating business code logic. 

    The version of the OpenAPI document: DEVELOP
    Contact: iparapheur@libriciel.coop
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from iparapheur_provisioning.models.tenant_representation import TenantRepresentation

class TestTenantRepresentation(unittest.TestCase):
    """TenantRepresentation unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TenantRepresentation:
        """Test TenantRepresentation
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TenantRepresentation`
        """
        model = TenantRepresentation()
        if include_optional:
            return TenantRepresentation(
                id = '',
                name = 'Example tenant'
            )
        else:
            return TenantRepresentation(
                name = 'Example tenant',
        )
        """

    def testTenantRepresentation(self):
        """Test TenantRepresentation"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
