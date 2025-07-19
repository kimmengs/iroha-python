import iroha2
from iroha2.data_model.isi import *
from iroha2.data_model.domain import *

domain = Domain("looking_glass")
register = Register(Expression(Value(Identifiable(domain))))
