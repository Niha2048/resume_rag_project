stateDiagram-v2
    [*] --> START
    START --> ParseJD
    ParseJD --> ExtractReqs
    ExtractReqs --> SearchResumes
    SearchResumes --> RankCandidates
    RankCandidates --> GenerateReport
    GenerateReport --> END

    note right of ExtractReqs
      Iterative refinement node
      can update requirements mid-flow
    end note

    note right of RankCandidates
      Explainability node
      answers "Why did X rank higher than Y"
    end note

    note right of GenerateReport
      Multi-round screening node
      layered filtering & hire/no-hire
    end note
