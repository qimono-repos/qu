import Std.Intrinsic.*;
import Std.Measurement.*;

@EntryPoint()
operation PhaseKickback() : Unit {
    Message("=== Phase Kickback Demonstration ===");

    use (eigen, target) = (Qubit(), Qubit());

    H(eigen);
    H(target);

    Controlled Z([eigen], target);

    H(eigen);
    H(target);

    let re = M(eigen);
    let rt = M(target);
    Message($"Measured: eigen={re}, target={rt}");

    Reset(eigen);
    Reset(target);
}
