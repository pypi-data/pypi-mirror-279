from pmix import *

#define a set of directives for pset operation requests */
#typedef uint8_t pmix_psetop_directive_t;

PMIX_PSETOP_NULL            =       0   # Invalid pset operation
PMIX_PSETOP_ADD             =       1   # Resources are added
PMIX_PSETOP_SUB             =       2   # Resources are removed
PMIX_PSETOP_REPLACE         =       3   # Resources are replaced
PMIX_PSETOP_MALLEABLE       =       4   # Resources are added or removed depending on scheduler decision
PMIX_PSETOP_GROW            =       5   # ADD + UNION
PMIX_PSETOP_SHRINK          =       6   # SUB + DIFFERENCE
PMIX_PSETOP_UNION           =       7   # The union of two psets is requested
PMIX_PSETOP_DIFFERENCE      =       8   # The difference of two psets is requested
PMIX_PSETOP_INTERSECTION    =       9   # The intersection of two psets is requested
PMIX_PSETOP_MULTI           =       10  # Multiple operations specified in the info object
PMIX_PSETOP_SPLIT           =       11  # Splt operation
PMIX_PSETOP_CANCEL          =       12  # Cancel PSet Operations
#define a value boundary beyond which implementers are free
#to define their own directive values */
PMIX_PSETOP_EXTERNAL        =       128

PMIX_EVENT_PSETOP_DEFINED   =       PMIX_EXTERNAL_ERR_BASE - 1
PMIX_EVENT_PSETOP_GRANTED   =       PMIX_EXTERNAL_ERR_BASE - 2
PMIX_EVENT_PSETOP_CANCELED  =       PMIX_EXTERNAL_ERR_BASE - 3
PMIX_EVENT_PSETOP_EXECUTED  =       PMIX_RC_FINALIZED
