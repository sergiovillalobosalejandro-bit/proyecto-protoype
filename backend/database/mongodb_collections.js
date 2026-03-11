// MongoDB Collections Structure for Clinical Intervention Tracking System

// Clinical History Collection
db.createCollection("historial_clinico", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["couder_id", "intervencion_id", "fecha_registro"],
      properties: {
        couder_id: { bsonType: "int" },
        intervencion_id: { bsonType: "int" },
        notas_completas: { bsonType: "string" },
        sintomas_observados: { bsonType: "array", items: { bsonType: "string" } },
        estado_emocional: { bsonType: "string" },
        nivel_participacion: { bsonType: "string" },
        observaciones_adicionales: { bsonType: "string" },
        fecha_registro: { bsonType: "date" },
        actualizado_en: { bsonType: "date" }
      }
    }
  }
});

// AI Analyses Collection
db.createCollection("ai_analisis", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["couder_id", "tipo_analisis", "fecha_generacion", "contenido"],
      properties: {
        couder_id: { bsonType: "int" },
        tipo_analisis: { bsonType: "string", enum: ["sintesis", "diagnostico", "sugerencias"] },
        contenido: {
          bsonType: "object",
          properties: {
            resumen: { bsonType: "string" },
            puntos_clave: { bsonType: "array", items: { bsonType: "string" } },
            diagnostico_preliminar: { bsonType: "string" },
            sugerencias: { bsonType: "array", items: { bsonType: "string" } },
            nivel_riesgo: { bsonType: "string", enum: ["bajo", "medio", "alto"] },
            recomendaciones: { bsonType: "array", items: { bsonType: "string" } }
          }
        },
        intervenciones_incluidas: { bsonType: "array", items: { bsonType: "int" } },
        fecha_generacion: { bsonType: "date" },
        modelo_ia: { bsonType: "string" },
        version: { bsonType: "string" },
        creado_por_usuario_id: { bsonType: "int" }
      }
    }
  }
});

// Audio Records Collection
db.createCollection("audio_registros", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["couder_id", "usuario_id", "fecha_grabacion", "archivo_path"],
      properties: {
        couder_id: { bsonType: "int" },
        usuario_id: { bsonType: "int" },
        intervencion_id: { bsonType: "int" },
        titulo: { bsonType: "string" },
        descripcion: { bsonType: "string" },
        archivo_path: { bsonType: "string" },
        duracion_segundos: { bsonType: "int" },
        formato: { bsonType: "string" },
        tamano_bytes: { bsonType: "long" },
        transcripcion: { bsonType: "string" },
        fecha_grabacion: { bsonType: "date" },
        fecha_transcripcion: { bsonType: "date" },
        estado: { bsonType: "string", enum: ["grabado", "procesando", "transcrito", "error"] },
        metadata: {
          bsonType: "object",
          properties: {
            calidad_audio: { bsonType: "string" },
            dispositivo_grabacion: { bsonType: "string" },
            ubicacion: { bsonType: "string" }
          }
        }
      }
    }
  }
});

// Progress Tracking Collection
db.createCollection("seguimiento_progreso", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["couder_id", "fecha_evaluacion", "metricas"],
      properties: {
        couder_id: { bsonType: "int" },
        fecha_evaluacion: { bsonType: "date" },
        metricas: {
          bsonType: "object",
          properties: {
            participacion: { bsonType: "double", minimum: 0, maximum: 10 },
            compromiso: { bsonType: "double", minimum: 0, maximum: 10 },
            progreso_academico: { bsonType: "double", minimum: 0, maximum: 10 },
            integracion_social: { bsonType: "double", minimum: 0, maximum: 10 },
            autoestima: { bsonType: "double", minimum: 0, maximum: 10 },
            motivacion: { bsonType: "double", minimum: 0, maximum: 10 }
          }
        },
        observaciones: { bsonType: "string" },
        evaluador_id: { bsonType: "int" },
        periodo_evaluacion: { bsonType: "string" },
        metas_alcanzadas: { bsonType: "array", items: { bsonType: "string" } },
        areas_mejora: { bsonType: "array", items: { bsonType: "string" } }
      }
    }
  }
});

// Create indexes for better performance
db.historial_clinico.createIndex({ "couder_id": 1, "fecha_registro": -1 });
db.historial_clinico.createIndex({ "intervencion_id": 1 });
db.historial_clinico.createIndex({ "fecha_registro": -1 });

db.ai_analisis.createIndex({ "couder_id": 1, "fecha_generacion": -1 });
db.ai_analisis.createIndex({ "tipo_analisis": 1 });
db.ai_analisis.createIndex({ "fecha_generacion": -1 });

db.audio_registros.createIndex({ "couder_id": 1, "fecha_grabacion": -1 });
db.audio_registros.createIndex({ "usuario_id": 1 });
db.audio_registros.createIndex({ "intervencion_id": 1 });
db.audio_registros.createIndex({ "fecha_grabacion": -1 });

db.seguimiento_progreso.createIndex({ "couder_id": 1, "fecha_evaluacion": -1 });
db.seguimiento_progreso.createIndex({ "evaluador_id": 1 });
db.seguimiento_progreso.createIndex({ "fecha_evaluacion": -1 });

// Sample data insertion (optional)
// db.historial_clinico.insertOne({
//   couder_id: 1,
//   intervencion_id: 1,
//   notas_completas: "El couder mostró mejoría en la participación...",
//   sintomas_observados: ["Ansiedad leve", "Dificultad de concentración"],
//   estado_emocional: "Estable",
//   nivel_participacion: "Moderado",
//   observaciones_adicionales: "Requiere seguimiento continuo",
//   fecha_registro: new Date(),
//   actualizado_en: new Date()
// });
