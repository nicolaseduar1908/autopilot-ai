import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MiAppIA());
}

class MiAppIA extends StatelessWidget {
  const MiAppIA({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Controlador IA',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        useMaterial3: true,
      ),
      home: const PantallaControlador(),
    );
  }
}

class PantallaControlador extends StatefulWidget {
  const PantallaControlador({super.key});

  @override
  State<PantallaControlador> createState() => _PantallaControladorState();
}

class _PantallaControladorState extends State<PantallaControlador> {
  final TextEditingController _controladorTexto = TextEditingController();
  String _respuestaIA = "";
  bool _cargando = false;

  // FUNCIÓN PARA ENVIAR COMANDOS GENERALES
  Future<void> enviarComando() async {
    final texto = _controladorTexto.text.trim();
    if (texto.isEmpty) return;

    setState(() {
      _cargando = true;
      _respuestaIA = "";
    });

    try {
      final url = Uri.parse('http://127.0.0.1:5000/api/comando');
      final respuesta = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'comando': texto}),
      );

      if (respuesta.statusCode == 200) {
        final datos = jsonDecode(respuesta.body);
        setState(() {
          _respuestaIA = datos['respuesta'] ?? 'Sin respuesta';
        });
      } else {
        setState(() {
          _respuestaIA = '⚠️ Error en el servidor: ${respuesta.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _respuestaIA = '❌ Error de conexión con el servidor: $e';
      });
    } finally {
      setState(() {
        _cargando = false;
      });
    }
  }

  // FUNCIÓN PARA EJECUTAR EL FLUJO COMPLETO DEL ORQUESTADOR Y MOSTRAR EL GUION
  Future<void> ejecutarOrquestador() async {
    setState(() {
      _cargando = true;
      _respuestaIA = "";
    });

    try {
      final url = Uri.parse('http://127.0.0.1:5000/orquestador/ejecutar_flujo_completo');
      final respuesta = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'nicho': 'Emprendimiento',
          'tema': 'Hotmart IA',
          'canal_id': 'canal_youtube_01',
          'avatar_id': 'avatar_vendedor',
        }),
      );

      if (respuesta.statusCode == 200) {
        final datos = jsonDecode(respuesta.body);
        final detalles = datos['detalles_ejecucion'] ?? {};
        final guion = detalles['guion_final'] ?? {};
        
        // Si el backend devuelve un guion estructurado, lo formateamos bonito:
        String textoGuion = "";
        if (guion.isNotEmpty) {
          textoGuion = """
🎬 GUION GENERADO PARA EL VIDEO:
• 🪝 Gancho: ${guion['gancho_inicial'] ?? ''}
• ⚠️ Problema: ${guion['problema'] ?? ''}
• 💡 Solución: ${guion['solucion'] ?? ''}
• 🚀 Llamado a la acción: ${guion['llamado_a_la_accion'] ?? ''}
""";
        }

        setState(() {
          _respuestaIA = """
🎉 ¡FLUJO Y GUION GENERADOS CON ÉXITO!

📌 Mensaje: ${datos['mensaje'] ?? 'Completado'}
📌 Estado: ${datos['status'] ?? 'Exitoso'}
📌 Nicho Objetivo: ${detalles['nicho_objetivo'] ?? 'N/A'}
📌 Tema: ${detalles['tema'] ?? 'N/A'}
📌 Canal Destino: ${detalles['canal_destino'] ?? 'N/A'}
📌 Avatar Asignado: ${detalles['avatar_asignado'] ?? 'N/A'}

$textoGuion
📋 PASOS COMPLETADOS:
${(detalles['pasos_completados'] as List?)?.map((p) => " • $p").join("\n") ?? "Ninguno"}
""";
        });
      } else {
        setState(() {
          _respuestaIA = '⚠️ Error en el servidor: ${respuesta.statusCode}';
        });
      }
    } catch (e) {
      setState(() {
        _respuestaIA = '❌ Error de conexión con el Orquestador: $e';
      });
    } finally {
      setState(() {
        _cargando = false;
      });
    }
  }

  // FUNCIÓN PARA COPIAR AL PORTAPAPELES
  void _copiarAlPortapapeles() {
    if (_respuestaIA.isNotEmpty) {
      Clipboard.setData(ClipboardData(text: _respuestaIA));
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('📋 ¡Respuesta copiada al portapapeles con éxito!'),
          duration: Duration(seconds: 2),
          backgroundColor: Colors.deepPurple,
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Copiloto de IA & Estrategia'),
        backgroundColor: Colors.deepPurple.shade100,
        actions: [
          if (_respuestaIA.isNotEmpty && !_cargando)
            IconButton(
              icon: const Icon(Icons.copy),
              tooltip: 'Copiar Respuesta Completa',
              onPressed: _copiarAlPortapapeles,
            ),
          IconButton(
            icon: const Icon(Icons.refresh),
            tooltip: 'Limpiar Pantalla',
            onPressed: () {
              setState(() {
                _controladorTexto.clear();
                _respuestaIA = "";
              });
            },
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // CAMPO DE CONSULTA
            TextField(
              controller: _controladorTexto,
              maxLines: 3,
              decoration: InputDecoration(
                labelText: 'Escribe tu comando o consulta estratégica...',
                hintText: 'Ej: Hazme un guión corto sobre superación',
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
            const SizedBox(height: 12),

            // BOTONES DE ACCIÓN
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                OutlinedButton.icon(
                  onPressed: _cargando ? null : ejecutarOrquestador,
                  icon: const Icon(Icons.auto_mode),
                  label: const Text('Ejecutar Orquestador'),
                  style: OutlinedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton.icon(
                  onPressed: _cargando ? null : enviarComando,
                  icon: const Icon(Icons.send),
                  label: Text(_cargando ? 'Procesando...' : 'Enviar a la IA'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.deepPurple,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),

            // BARRA DE ACCIÓN SOBRE LA RESPUESTA
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(
                color: Colors.deepPurple.shade50,
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'Respuesta del Servidor / IA:',
                    style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  if (_respuestaIA.isNotEmpty && !_cargando)
                    ElevatedButton.icon(
                      onPressed: _copiarAlPortapapeles,
                      icon: const Icon(Icons.copy, size: 16),
                      label: const Text('Copiar'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.deepPurple,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                      ),
                    ),
                ],
              ),
            ),
            const SizedBox(height: 10),

            // ÁREA DE CONTENIDO CON SCROLL
            Expanded(
              child: Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.grey.shade300),
                ),
                child: _cargando
                    ? const Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            CircularProgressIndicator(),
                            SizedBox(height: 12),
                            Text('Procesando solicitud con el servidor...'),
                          ],
                        ),
                      )
                    : SingleChildScrollView(
                        physics: const BouncingScrollPhysics(),
                        child: SelectableText(
                          _respuestaIA.isEmpty
                              ? 'Escribe una consulta o presiona "Ejecutar Orquestador" para iniciar.'
                              : _respuestaIA,
                          style: const TextStyle(
                            fontSize: 15,
                            height: 1.5,
                            color: Colors.black87,
                          ),
                        ),
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}