Lemma ex1: forall A, ~~~A -> ~A.
Proof.
intro.
intro.
intro.
destruct H.
intro.
destruct H.
apply H0.
Qed.

Lemma ex2: forall A B, A \/ B -> ~(~A /\ ~B).
Proof.
intro.
intro.
intro.
intro.
destruct H0.
destruct H.
destruct H0.
apply H.
destruct H1.
apply H.
Qed.

Lemma ex3: forall T (P:T -> Prop),
(~ exists x, P x) -> forall x, ~P x.
Proof.
intro.
intro.
intro.
intro.
intro.
destruct H.
exists x.
apply H0.
Qed.