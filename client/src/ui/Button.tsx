import {
  ButtonHTMLAttributes,
  DetailedHTMLProps,
  PropsWithChildren,
} from "react";
import styled from "styled-components";

const Loader = styled.div`
  & {
    position: absolute;
    color: #ffffff;
    top: 1.25rem;
    left: 1.25rem;
  }
  &,
  &:after {
    box-sizing: border-box;
  }
  & {
    display: inline-block;
    width: 40px;
    height: 40px;
  }
  &:after {
    content: " ";
    display: block;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    border: 3px solid currentColor;
    border-color: currentColor transparent currentColor transparent;
    animation: lds-dual-ring 1.2s linear infinite;
  }
  @keyframes lds-dual-ring {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
`;

const RawButton = styled.button`
  padding-left: 3.5rem;
  padding-right: 3.5rem;
  border: 1px solid white;
  border-radius: 0.5rem;
  color: white;
  padding-top: 1.25rem;
  padding-bottom: 1.25rem;
  position: relative;
  transition: box-shadow 0.1s linear;

  &:hover {
    box-shadow: 0 0 5px 5px #ffffff55;
  }
`;

export default function Button({
  children,
  loading,
  onClick,
}: PropsWithChildren<{ loading?: boolean; onClick: () => void }>) {
  return (
    <RawButton onClick={onClick}>
      {loading && <Loader />}
      {children}
    </RawButton>
  );
}
