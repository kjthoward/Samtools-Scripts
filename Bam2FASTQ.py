try:
        import os, subprocess, tkFileDialog, Tkinter, textwrap, textwrap, pdb, time
        from Bio import SeqIO
except:
        print("Some modules could not be imported")
        print("Please re-the 'Get Python Packages' file in the NGS Computer Folder")
        raw_input("Press Enter to Quit: ")
        sys.exit()
rootwindow = Tkinter.Tk()
rootwindow.withdraw()

#change this depending on where samtools is installed. Everything else is dynamic/selected during use
samtools_location="D:\\samtools"
FASTQ_Count=0
def Q_Letter(score):
	return chr(score+33)
                 
os.system("title FASTQ from BAMs")
try:
        os.chdir(samtools_location)
except:
        print ("Samtools directory not found. Please check location or re-place samtools folder")
        raw_input("Press Enter to Quit: ")
        sys.exit()
print("Please select of folder of BAM files")
path=tkFileDialog.askdirectory(parent=rootwindow, title='Please select a folder of BAM files')

for root, dirnames, filenames in os.walk(path):
    for filename in filenames:
        if filename[-4:]==".bam":
##                pdb.set_trace()
                temp_fastq=[]
                #Orders the BAM
                sort_command=["samtools", "sort", "-n", "{}".format(os.path.join(root,os.path.dirname(filename),filename)),
                     "-o", "{}".format(os.path.join(root,os.path.dirname(filename),filename[:-4]+"_sorted.bam")), "-O", "BAM"]
                p=subprocess.Popen(sort_command, shell=True)
                print("Creating Ordered BAM for {}".format(filename))
                p.wait()
                f=os.path.join(root,filename[:-4]+"_sorted.bam")
                print("Creating FASTQ files for {}".format(os.path.split(filename)[1]))
                #Makes FASTQ files from the ordered BAMs and deletes ordered bams after
                command=["samtools", "fastq", 
                         "-1", "{}".format(os.path.join(root, os.path.dirname(f),"_".join(os.path.split(f)[1].split("_")[0:2])+"_L001_R1_001_TEMP.fastq")),
                         "-2", "{}".format(os.path.join(root, os.path.dirname(f),"_".join(os.path.split(f)[1].split("_")[0:2])+"_L001_R2_001_TEMP.fastq")),
                         "{}".format(f)]
                p2=subprocess.Popen(command, shell=True)
                
                p2.wait()
                temp_fastq+=[os.path.join(root, os.path.dirname(f),"_".join(os.path.split(f)[1].split("_")[0:2])+"_L001_R1_001_TEMP.fastq"),os.path.join(root, os.path.dirname(f),"_".join(os.path.split(f)[1].split("_")[0:2])+"_L001_R2_001_TEMP.fastq")]
                os.remove(f)

                #Makes the final FASTQ files from the temp files by including the CASAVA 1.8 tag (1:N:0:<SAMPLE NUMBER>)
                #Then removes the temp fastq (sleep first to ensure it's done being used)
                #Gets sample number from file name
                for fastq in temp_fastq:
                        sample_number=os.path.split(fastq)[1].split("_")[1].strip("S")
                        new=open(os.path.join(os.path.split(fastq)[0],("_").join(os.path.split(fastq)[1].split("_")[0:4])+"_001.fastq"),"w")
                        for record in SeqIO.parse(fastq,"fastq"):
                                header=record.id
                                header="@{0} 1:N:0:{1}".format(header,sample_number)
                                scores=""
                                #Couldn't find a way to get Q Score characters from SeqIO, so gets numbers then Phred33 Converts to ASCII
                                for value in record.letter_annotations["phred_quality"]:
                                        scores+=Q_Letter(value)
                                new.write("{0}\n{1}\n+\n{2}\n".format(header,record.seq,scores))
                        FASTQ_Count+=0.5
                        new.close()
                        time.sleep(3)
                        os.remove(fastq)                                 

if FASTQ_Count>0:
    print textwrap.fill("Successfully created .FASTQ files for {} .bam files".format(FASTQ_Count))
elif FASTQ_Count==0:
    print textwrap.fill("No .bam files could be found in {}, or it's subfolders. Please check the folder and try again".format(path))

raw_input("Press enter to quit: ")
    


        
