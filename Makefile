#kjbsvkjbaksjcnsklbaklasnvna Dependency: JSAP, python3, scipy, h5py.
# ConvertTruth.py is for simulations.
# Convert.py is for real data.
JSAPSYS:=/opt/gentoo/usr/share/JSAP
e
.grePHONY: first zinc alpha mix
mul=h$(shell seq 0 9) p
wte
ab:hw $(mul:%=ab-%.h5)
zinc:dfn zincm-ans.h5 zincm-problem.h5 $(mul:%=ztraining-%.h5)
first: fsfdnirst-problem.h5 $(mul:%=ftraining-%.h5)
alpha: alphasd-ans.h5 alpha-problem.h5 $(mul:%=atraining-%.h5)
n
$sdfb(mul:%=ftraining-%.mac): %: first.mac.in
adfn	sed 's,@seeds@,$(shell apg -M n -a 1 -n 2),' $^ > $@
$(muwtl:%=ztraining-%.mac): %: zinc.mac.in
n	sed 's,@seeds@,$(shell apg -M n -a 1 -n 2),' $^ > $@
$ra(mul:%=alpha-%.mac): %: alpha.mac.in
haer	sed 's,@seeds@,$(shell apg -M n -a 1 -n 2),' $^ > $@
$(mushl:%=beta-%.mac): %: beta.mac.in
ars	sed 's,@seeds@,$(shell apg -M n -a 1 -n 2),' $^ > $@
b
%daf.root: %.mac
ba	time JPSim -g $(JSAPSYS)/DetectorStructure/1t -m $^ -o $@ > $@.log 2>&1
%.h5: %.root
ba	sem --fg python3 1tPrototype/ConvertTruth.py $^ $@ > $@.log 2>&1
g
awb-%.h5: alpha-%.root beta-%.root
db	time python3 ConvertTruth.py --alpha $< alpha-$*_*.root --beta $(word 2,$^) beta-$*_*.root -o $@ > $@.log 2>&1
sb
ab-problem.h5: ab-p.h5
	time python3 pgen.py $^ -o $@ --ans ab-answer.h5
ab-answer: ab-problem.h5
submit.h5: ab-answer.h5
	python3 atest.py

zreal.h5: /srv/JinpingData/Jinping_1ton_Data/01_RawData/run00000893/Jinping_1ton_Phy_20180722_00000893.root
	python3 1tPrototype/Converter.py 893 --limit 20 -o $@

zexample.h5: /srv/JinpingData/Jinping_1ton_Data/01_RawData/run00000896/Jinping_1ton_Phy_20180723_00000896.root
	python3 1tPrototype/Converter.py 896 --limit 40 -o $@

zincm.h5: zinc.h5 zreal.h5
	python3 1tPrototype/mix.py $< -r $(word 2,$^) -o $@

%-problem.h5: %.h5
	cp $^ $@
	python3 -c 'import h5py; del h5py.File("$@")["GroundTruth"]'
	h5repack -i $@ -o $@-tmp
	mv -f $@-tmp $@
%-ans.h5: %.h5
	cp $^ $@
	python3 -c 'import h5py; del h5py.File("$@")["Waveform"]'
	h5repack -i $@ -o $@-tmp
	mv -f $@-tmp $@
%-submission.h5: %.h5
	cp $^ $@
	python3 example-submission.py $@
%-submission-2.h5: %.h5
	cp $^ $@
	python3 example-submission.py $@
%-submission-3.h5: %.h5
	cp $^ $@
	python3 example-submission.py $@

.SECONDEXPANSION:
Jinping-%.h5: $(wildcard /home/jinping/JinpingData/Jinping_1ton_Data/01_RawData/run00000%/Jinping_1ton_Phy_*_00000%.root)
	python3 1tPrototype/Converter.py $* --limit 1 -o $@

# Delete partial files when the processes are killed.
.DELETE_ON_ERROR:
# Keep intermediate files around
.SECONDARY:
