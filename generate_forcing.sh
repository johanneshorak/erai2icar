while [[ $# > 1 ]]
do
	key="$1"

	case $key in
		-r|--region)
		REGION="$2"
		shift # past argument
		;;
		-d|--dates)
		DATES="$2"
		shift # past argument
		;;
		-o|--out)
		outfile="$2"
		shift # past argument
		;;
		*)
				# unknown option
		;;
	esac
	shift # past argument or value
done


if [ -z "$REGION" ] && [ -z "$DATES"]; then
  echo ""
  echo "error: domain boundaries and timeframe have to be specified!"
  echo ""
  echo "usage: generate_forcing.sh -r N/W/S/E -d YYYY-MM-DD/to/YYYY-MM-DD outputfilename"
  echo "  N/W/S/E ... northern/western/southern/eastern longitude/latitude of domain"
  echo ""
  exit
fi

echo "specified region: $REGION"
echo "specified dates : $DATES"
echo "specified outfile: $outfile"

echo "retrieving erainterim reanalysis..."
python ./retrieve_erainterim.py $REGION $DATES $outfile
echo "...[done]"

echo "assembling forcing..."
python ./forcing_assembly.py erai_atm.nc erai_sfc.nc $outfile
echo "...[done]" 

