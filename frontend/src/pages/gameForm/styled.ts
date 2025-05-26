import styled from "styled-components";

const Container = styled.div`
  margin-top: 20px;
  display: flex;
  justify-content: center;
`;

const TitleContainer = styled.div`
  display: flex;
  text-align: center;
  justify-content: center;
`;

const Title = styled.text`
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
`;

const Label = styled.text`
  font-size: 16px;
  font-weight: bold;
  text-decoration: underline;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  width: 400px;
  gap: 10px;
`;

const Input = styled.input`
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border-radius: 8px;
  border: none;
  border: 1px solid #eaeaea;
  margin-bottom: 4px;
`;

const ButtonContainer = styled.div`
  margin-top: 4px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const Button = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  background-color: orange;
  color: black;
  border: none;
  cursor: pointer;
  font-weight: bold;
  width: 50%;
  border-radius: 8px;
  &:hover {
    background-color: darkorange;
    transform: scale(1.1);
  }
`;

export {
  Container,
  Button,
  Form,
  Input,
  Label,
  Title,
  ButtonContainer,
  TitleContainer,
};
