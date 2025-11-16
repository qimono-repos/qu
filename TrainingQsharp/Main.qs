namespace TrainingQsharp {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Canon;
    open TrainingQsharp.RandomUtils;

    operation MainMeasure() : Int {

        let max = 100;
        Message($"Generating a random number between 0 and {max}: ");

        return GenerateRandomNumberInRange(max);


    }
}
