from CP3SlurmUtils.Configuration import Configuration

config = Configuration()

#--------------------------------------------------------------------------------
# 1. SLURM sbatch command options
#--------------------------------------------------------------------------------

config.sbatch_partition = "cp3"
config.sbatch_qos = "cp3"
config.sbatch_time = "0-00:05"
config.sbatch_memPerCPU = "1024"
config.sbatch_chdir = "."
config.sbatch_output = "/dev/null"
config.sbatch_error = "/dev/null"
config.sbatch_additionalOptions = []

#--------------------------------------------------------------------------------
# 2. User batch script parameters
#--------------------------------------------------------------------------------

config.batchScriptsDir = config.sbatch_chdir + "/slurm_batch_scripts"
config.batchScriptsFilename = ""

config.inputSandboxContent = []
config.inputSandboxDir = config.sbatch_chdir + "/slurm_input_sandboxes"
config.inputSandboxFilename = ""

config.scratchDir = "${LOCALSCRATCH}"
config.handleScratch = False

config.writeLogsOnWN = True
config.separateStdoutStderrLogs = False
config.stdoutFilename = ""
config.stderrFilename = ""

config.environmentType = ""
config.cmsswDir = ""

config.useJobArray = True
config.maxRunningJobs = None
# 2 jobs will be submitted, because the config parameter 'inputParams' has length 2.
config.numJobs = None

config.stageout = True
config.stageoutFiles = ["output_file_for_job_*.txt"]
# We chose the filename of the outputs to be independent of the job (array) id number.
# So let's put the output files in a directory whose name contains the job (array) id number.
if config.useJobArray:
    config.stageoutDir = config.sbatch_chdir + "/slurm_outputs/job_array_${SLURM_ARRAY_JOB_ID}"
else:
    config.stageoutDir = config.sbatch_chdir + "/slurm_outputs/job_${SLURM_JOB_ID}"

config.stageoutLogs = True
# The default filename of the SLURM logs has already a job (array) id number (and a job array task id number) in it.
# So we can put all logs together in a unique directory; they won't overwrite each other.
config.stageoutLogsDir = config.sbatch_chdir + "/slurm_logs"

config.inputParamsNames = ["outputFile"]
config.inputParams = [["output_file_for_job_1.txt"], ["output_file_for_job_2.txt"]]
config.putInputParamsInBatchScript = False
config.inputParamsFilename = ""

config.apptainer = False
config.apptainerImage = ""

# For job number 1, the environment variable "outputFile" will be equal to "output_file_for_job_1.txt".
# For job number 2, the environment variable "outputFile" will be equal to "output_file_for_job_2.txt".
# The payload will have access to environment variables like 'SLURM_JOB_ID', 'SLURM_ARRAY_JOB_ID'
# and 'SLURM_ARRAY_TASK_ID', so we can use those variables here.
if config.useJobArray:
    config.payload = \
"""
echo "Start of 'Hello World' user payload for job ${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}"
echo "Hello World! I am a SLURM job with ID ${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}" > ${outputFile}
echo "  End of 'Hello World' user payload for job ${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}"
"""
else:
    config.payload = \
"""
echo "Start of 'Hello World' user payload for job ${SLURM_JOB_ID}"
echo "Hello World! I am a SLURM job with ID ${SLURM_JOB_ID}" > ${outputFile}
echo "  End of 'Hello World' user payload for job ${SLURM_JOB_ID}"
"""
