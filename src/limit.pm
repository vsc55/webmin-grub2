#### limit virutal memory resources
use BSD::Resource;
setrlimit(get_rlimits()->{RLIMIT_VMEM}, 1_000_000_000, -1) or die;
#### end limit
