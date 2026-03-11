-- PostgreSQL Schema for Clinical Intervention Tracking System

-- Enable UUID extension if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Sedes (Educational Centers)
CREATE TABLE IF NOT EXISTS sedes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    direccion VARCHAR(500),
    telefono VARCHAR(50),
    email VARCHAR(255),
    activa BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP WITH TIME ZONE
);

-- Cortes (Time-based cohorts)
CREATE TYPE tipo_ruta AS ENUM ('basica', 'avanzada');

CREATE TABLE IF NOT EXISTS cortes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    sede_id INTEGER REFERENCES sedes(id) ON DELETE CASCADE,
    fecha_inicio TIMESTAMP WITH TIME ZONE NOT NULL,
    fecha_fin TIMESTAMP WITH TIME ZONE NOT NULL,
    tipo_ruta tipo_ruta NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP WITH TIME ZONE
);

-- Clanes (Subgroups within cortes)
CREATE TYPE jornada AS ENUM ('AM', 'PM');

CREATE TABLE IF NOT EXISTS clanes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    corte_id INTEGER REFERENCES cortes(id) ON DELETE CASCADE,
    jornada jornada NOT NULL,
    capacidad_maxima INTEGER DEFAULT 30,
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP WITH TIME ZONE
);

-- Usuarios (System users)
CREATE TYPE rol_usuario AS ENUM ('admin', 'terapista', 'coordinador');

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    rol rol_usuario DEFAULT 'terapista',
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP WITH TIME ZONE
);

-- Couders (Participants)
CREATE TYPE estado_couder AS ENUM ('activo', 'retirado', 'completado');

CREATE TABLE IF NOT EXISTS couders (
    id SERIAL PRIMARY KEY,
    cc VARCHAR(50) UNIQUE NOT NULL,
    nombre_completo VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE,
    telefono VARCHAR(50),
    email VARCHAR(255),
    direccion VARCHAR(500),
    clan_id INTEGER REFERENCES clanes(id) ON DELETE CASCADE,
    estado estado_couder DEFAULT 'activo',
    fecha_ingreso TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_retiro TIMESTAMP WITH TIME ZONE,
    fecha_completado TIMESTAMP WITH TIME ZONE,
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP WITH TIME ZONE
);

-- Intervenciones (Intervention records)
CREATE TABLE IF NOT EXISTS intervenciones (
    id SERIAL PRIMARY KEY,
    couder_id INTEGER REFERENCES couders(id) ON DELETE CASCADE,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    observaciones TEXT,
    fecha_intervencion TIMESTAMP WITH TIME ZONE NOT NULL,
    duracion_minutos INTEGER,
    tipo_intervencion VARCHAR(100),
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_sedes_nombre ON sedes(nombre);
CREATE INDEX IF NOT EXISTS idx_cortes_sede_id ON cortes(sede_id);
CREATE INDEX IF NOT EXISTS idx_cortes_tipo_ruta ON cortes(tipo_ruta);
CREATE INDEX IF NOT EXISTS idx_clanes_corte_id ON clanes(corte_id);
CREATE INDEX IF NOT EXISTS idx_clanes_jornada ON clanes(jornada);
CREATE INDEX IF NOT EXISTS idx_couders_cc ON couders(cc);
CREATE INDEX IF NOT EXISTS idx_couders_clan_id ON couders(clan_id);
CREATE INDEX IF NOT EXISTS idx_couders_estado ON couders(estado);
CREATE INDEX IF NOT EXISTS idx_intervenciones_couder_id ON intervenciones(couder_id);
CREATE INDEX IF NOT EXISTS idx_intervenciones_usuario_id ON intervenciones(usuario_id);
CREATE INDEX IF NOT EXISTS idx_intervenciones_fecha ON intervenciones(fecha_intervencion);

-- Create trigger for updating actualizado_en timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for all tables with actualizado_en
CREATE TRIGGER update_sedes_actualizado_en BEFORE UPDATE ON sedes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_cortes_actualizado_en BEFORE UPDATE ON cortes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_clanes_actualizado_en BEFORE UPDATE ON clanes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_usuarios_actualizado_en BEFORE UPDATE ON usuarios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_couders_actualizado_en BEFORE UPDATE ON couders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_intervenciones_actualizado_en BEFORE UPDATE ON intervenciones FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
