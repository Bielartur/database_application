import { Form, Button, Input } from "./styled";
import { useNavigate } from "react-router-dom";
export function Login() {
  const navigate = useNavigate();
  function handleLogin() {
    navigate("/home");
  }

  return (
    <>
      <Form>
        <Input type="text" placeholder="Usuário" required />
        <Input type="password" placeholder="Senha" required />
        <Button type="button" onClick={handleLogin}>
          Entrar
        </Button>
      </Form>

      <p>ASDASKDAOSDKAOSDKADOK</p>
    </>
  );
}
