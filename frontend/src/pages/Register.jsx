import React, { useState, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        cpf: '',
        telefone: ''
    });
    const { register } = useContext(AuthContext);
    const navigate = useNavigate();
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await register(formData);
            navigate('/');
        } catch (err) {
            setError('Erro ao criar conta. Verifique os dados.');
            console.error(err);
        }
    };

    const inputClass = "w-full px-4 py-3 bg-[#1a1a1a] border border-[#333] text-white placeholder-gray-500 rounded-lg focus:outline-none focus:border-[#d4af37] transition";

    return (
        <div className="min-h-screen flex items-center justify-center bg-[#0a0a0a] py-12 px-4 sm:px-6 lg:px-8">
            <div className="max-w-md w-full space-y-8">
                <div className="text-center">
                    <h1 className="text-3xl font-black text-gradient mb-2">GBLACK</h1>
                    <h2 className="text-xl text-white">
                        Criar nova conta
                    </h2>
                </div>
                <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
                    <input
                        name="username"
                        type="text"
                        required
                        className={inputClass}
                        placeholder="Usuário"
                        onChange={handleChange}
                    />
                    <input
                        name="email"
                        type="email"
                        required
                        className={inputClass}
                        placeholder="Email"
                        onChange={handleChange}
                    />
                    <input
                        name="password"
                        type="password"
                        required
                        className={inputClass}
                        placeholder="Senha"
                        onChange={handleChange}
                    />
                    <div className="grid grid-cols-2 gap-4">
                        <input
                            name="cpf"
                            type="text"
                            required
                            className={inputClass}
                            placeholder="CPF"
                            onChange={handleChange}
                        />
                        <input
                            name="telefone"
                            type="text"
                            required
                            className={inputClass}
                            placeholder="Telefone"
                            onChange={handleChange}
                        />
                    </div>

                    {error && <div className="text-red-500 text-sm text-center">{error}</div>}

                    <button
                        type="submit"
                        className="btn-primary w-full"
                    >
                        Cadastrar
                    </button>

                    <div className="text-center">
                        <Link to="/login" className="text-sm text-[#d4af37] hover:underline">
                            Já tem uma conta? Entre
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Register;
