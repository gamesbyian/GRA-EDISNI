// Ghidra headless postScript on explicitly local native binaries.
// Outputs only addresses, marker terms, and xref counts. No source dump.
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.symbol.ReferenceIterator;
import java.io.File;
import java.io.PrintWriter;
import java.util.Locale;

public class InspectConsumerStrings extends GhidraScript {
    private static final String[] MARKERS = {
        "password", "validate", "sequence", "secret", "input", "printer",
        "easteregg", "controller", "unlock", "branch"
    };
    private String csv(String val) {
        return "\"" + val.replace("\"", "\"\"").replace("\r", " ").replace("\n", " ") + "\"";
    }
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length != 1)
            throw new IllegalArgumentException("Expected one local CSV output path");
        int findings = 0;
        try (PrintWriter f = new PrintWriter(new File(args[0]), "UTF-8")) {
            f.println("address,matched_keyword,cross_reference_count");
            DataIterator it = currentProgram.getListing().getDefinedData(true);
            while (it.hasNext() && !monitor.isCancelled()) {
                Data data = it.next();
                Object value = data.getValue();
                if (!(value instanceof String)) continue;
                String lower = ((String)value).toLowerCase(Locale.ROOT);
                for (String marker : MARKERS) {
                    if (!lower.contains(marker)) continue;
                    int refs = 0;
                    ReferenceIterator xs = currentProgram.getReferenceManager().getReferencesTo(data.getAddress());
                    while (xs.hasNext() && refs < 10000) {
                        xs.next();
                        refs++;
                    }
                    f.println(csv(data.getAddress().toString()) + "," + csv(marker) + "," + refs);
                    if (++findings >= 2000) break;
                }
                if (findings >= 2000) break;
            }
        }
        println("INSIDE_CONSUMER_TRIAGE: " + findings + " matches; no validation path certified");
    }
}
